#!/usr/bin/env python3
import hashlib
import io
import json
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "mappings" / "design" / "real-sample-manifest.json"
OUT = ROOT / "validation-results" / "real-samples"
NORMALIZED = OUT / "normalized"
CACHE = OUT / "source-cache"


def stable_hash(namespace, value):
    return hashlib.sha256(f"{namespace}|{value}".encode("utf-8")).hexdigest()[:24]


def canonical_sha(records):
    payload = "\n".join(json.dumps(r, sort_keys=True, ensure_ascii=False, default=str) for r in records)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records), encoding="utf-8")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def amazon_sample(cfg):
    endpoint = "https://datasets-server.huggingface.co/first-rows"
    params = {"dataset": cfg["source"], "config": cfg["config"], "split": cfg["split"]}
    response = requests.get(endpoint, params=params, timeout=120)
    response.raise_for_status()
    body = response.json()
    raw = [entry["row"] for entry in body.get("rows", [])][: int(cfg["targetRecords"])]
    if len(raw) < min(10, int(cfg["targetRecords"])):
        raise RuntimeError(f"Amazon acquisition returned too few rows: {len(raw)}")

    normalized = []
    for row in raw:
        asin = row.get("asin") or "missing-asin"
        parent = row.get("parent_asin") or asin
        normalized.append({
            "synthetic": False,
            "rating": row.get("rating"),
            "title": "",
            "text": "",
            "images": [],
            "asin": stable_hash("amazon-asin", asin),
            "parent_asin": stable_hash("amazon-parent", parent),
            "user_id": stable_hash("amazon-user", row.get("user_id") or "opaque"),
            "timestamp": row.get("timestamp"),
            "verified_purchase": bool(row.get("verified_purchase")),
            "helpful_vote": int(row.get("helpful_vote") or 0)
        })

    revision = None
    try:
        info = requests.get(f"https://huggingface.co/api/datasets/{cfg['source']}", timeout=60)
        if info.ok:
            revision = info.json().get("sha")
    except requests.RequestException:
        pass

    return normalized, {
        "source": cfg["source"], "config": cfg["config"], "split": cfg["split"],
        "endpoint": response.url, "sourceRevision": revision,
        "selectedRecords": len(raw), "rawSelectionSha256": canonical_sha(raw),
        "selection": "first N rows returned by datasets-server first-rows API"
    }


def get_with_https_fallback(url, *, timeout=180):
    candidates = [url]
    if url.startswith("http://"):
        candidates.insert(0, "https://" + url[len("http://"):])
    errors = []
    for candidate in candidates:
        try:
            response = requests.get(candidate, timeout=timeout)
            if response.ok:
                return response, candidate
            errors.append(f"{candidate}: HTTP {response.status_code}")
        except requests.RequestException as exc:
            errors.append(f"{candidate}: {type(exc).__name__}: {exc}")
    raise RuntimeError("All source URL attempts failed: " + " | ".join(errors))


def subreddit_url(subreddit):
    base = "http://zissou.infosci.cornell.edu/convokit/datasets/subreddit-corpus/"
    response, _ = get_with_https_fallback(base + "subreddit-groupings.txt", timeout=120)
    groups = [line.strip() for line in response.text.splitlines() if line.strip()]
    for group in groups:
        bounds = group.split("~-~")
        if bounds[0] <= subreddit <= bounds[-1]:
            return base + "corpus-zipped/" + quote(group, safe="~-_") + "/" + quote(subreddit, safe="_-.") + ".corpus.zip"
    raise RuntimeError(f"Subreddit {subreddit} was not found in ConvoKit grouping index")


def wikiconv_url(name):
    parts = name.split("-")
    if len(parts) != 3:
        raise ValueError(f"Expected wikiconv-<language>-<year>, got {name}")
    _, language, year = parts
    return f"http://zissou.infosci.cornell.edu/convokit/datasets/wikiconv-corpus/corpus-zipped/{language}/wikiconv-{year}/full.corpus.zip"


def download_corpus_zip(name):
    if name.startswith("subreddit-"):
        url = subreddit_url(name.split("-", 1)[1])
    elif name.startswith("wikiconv-"):
        url = wikiconv_url(name)
    else:
        raise ValueError(f"Unsupported ConvoKit corpus name: {name}")

    response, used_url = get_with_https_fallback(url, timeout=300)
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{name}.zip"
    path.write_bytes(response.content)
    return path, used_url, hashlib.sha256(response.content).hexdigest()


def read_utterances_from_zip(path, *, wiki=False):
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
        jsonl = next((n for n in names if n.endswith("utterances.jsonl")), None)
        json_file = next((n for n in names if n.endswith("utterances.json")), None)
        if jsonl:
            raw_rows = [json.loads(line) for line in archive.read(jsonl).decode("utf-8").splitlines() if line.strip()]
        elif json_file:
            loaded = json.loads(archive.read(json_file).decode("utf-8"))
            raw_rows = loaded if isinstance(loaded, list) else list(loaded.values())
        else:
            raise RuntimeError(f"No utterances.jsonl/json found in {path.name}; members={names[:20]}")

    rows = []
    for raw in raw_rows:
        speaker = raw.get("speaker")
        if isinstance(speaker, dict):
            speaker = speaker.get("id") or speaker.get("name")
        meta = raw.get("meta") or {}
        row = {
            "id": str(raw.get("id")),
            "speaker": str(speaker or "opaque"),
            "conversation_id": str(raw.get("conversation_id")),
            "reply_to": None if raw.get("reply_to") is None else str(raw.get("reply_to")),
            "timestamp": raw.get("timestamp"),
            "text": raw.get("text") or "",
            "meta": meta,
        }
        if wiki:
            row["type"] = raw.get("type") or meta.get("type") or ""
        rows.append(row)
    return rows


def select_nested_conversations(rows, max_conversations, max_comments, *, wiki=False):
    groups = defaultdict(list)
    for row in rows:
        groups[str(row["conversation_id"])].append(row)

    selected = []
    selected_groups = 0
    for conversation_id in sorted(groups):
        group = groups[conversation_id]
        by_id = {r["id"]: r for r in group}
        root = by_id.get(conversation_id)
        if root is None:
            continue
        candidate_comments = [r for r in group if r["id"] != conversation_id]
        if wiki:
            candidate_comments = [r for r in candidate_comments if not bool((r.get("meta") or {}).get("is_section_header", False))]
        candidate_ids = {r["id"] for r in candidate_comments}
        nested = next((r for r in candidate_comments if r.get("reply_to") in candidate_ids), None)
        if nested is None:
            continue
        parent = by_id.get(nested["reply_to"])
        chosen = [root]
        for r in (parent, nested):
            if r and r not in chosen:
                chosen.append(r)
        ordered = sorted(candidate_comments, key=lambda r: ((r.get("timestamp") or 0), r["id"]))
        for r in ordered:
            if r not in chosen and len(chosen) - 1 < max_comments:
                chosen.append(r)
        selected.extend(chosen)
        selected_groups += 1
        if selected_groups >= max_conversations:
            break

    if selected_groups == 0:
        raise RuntimeError("No conversation with a resolvable nested reply was found in the bounded corpus")
    return selected, selected_groups


def normalize_conversation_rows(dataset, raw, *, wiki=False):
    id_map = {r["id"]: stable_hash(f"{dataset}-utterance", r["id"]) for r in raw}
    conv_map = {r["conversation_id"]: stable_hash(f"{dataset}-conversation", r["conversation_id"]) for r in raw}
    normalized = []
    for r in raw:
        meta = r.get("meta") or {}
        base = {
            "synthetic": False,
            "id": id_map[r["id"]],
            "speaker": stable_hash(f"{dataset}-speaker", r.get("speaker") or "opaque"),
            "conversation_id": conv_map[r["conversation_id"]],
            "reply_to": id_map.get(r.get("reply_to")) if r.get("reply_to") else None,
            "timestamp": r.get("timestamp"),
            "text": "",
            "meta": {}
        }
        if wiki:
            base["type"] = r.get("type") or ""
            base["meta"] = {
                "is_section_header": bool(meta.get("is_section_header", False)),
                "indentation": meta.get("indentation"),
                "rev_id": meta.get("rev_id"),
                "toxicity": meta.get("toxicity")
            }
        else:
            tlc = meta.get("top_level_comment")
            base["meta"] = {
                "score": int(meta.get("score") or 0),
                "top_level_comment": id_map.get(str(tlc)) if tlc is not None else None
            }
        normalized.append(base)
    return normalized


def corpus_sample(cfg, dataset, *, wiki=False):
    path, source_url, archive_sha = download_corpus_zip(cfg["source"])
    corpus_rows = read_utterances_from_zip(path, wiki=wiki)
    raw, conversations = select_nested_conversations(
        corpus_rows, int(cfg["maxConversations"]), int(cfg["maxCommentsPerConversation"]), wiki=wiki
    )
    normalized = normalize_conversation_rows(dataset, raw, wiki=wiki)
    return normalized, {
        "source": cfg["source"], "sourceUrl": source_url,
        "downloadArchiveSha256": archive_sha,
        "corpusUtterancesRead": len(corpus_rows),
        "selectedRecords": len(raw), "selectedConversations": conversations,
        "rawSelectionSha256": canonical_sha(raw),
        "selection": "first lexicographically ordered conversations with a resolvable nested reply; bounded by manifest limits"
    }


def main():
    cfg = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    provenance = {
        "evidenceVersion": cfg["evidenceVersion"],
        "acquiredAt": datetime.now(timezone.utc).isoformat(),
        "privacyPolicy": cfg["privacyPolicy"],
        "datasets": {}
    }

    amazon, amazon_meta = amazon_sample(cfg["datasets"]["amazon-reviews-2023"])
    reddit, reddit_meta = corpus_sample(cfg["datasets"]["reddit-convokit"], "reddit-convokit", wiki=False)
    wiki, wiki_meta = corpus_sample(cfg["datasets"]["wikiconv"], "wikiconv", wiki=True)

    for dataset, rows, meta in [
        ("amazon-reviews-2023", amazon, amazon_meta),
        ("reddit-convokit", reddit, reddit_meta),
        ("wikiconv", wiki, wiki_meta),
    ]:
        path = NORMALIZED / f"{dataset}.jsonl"
        transformed_sha = write_jsonl(path, rows)
        meta["normalizedRecords"] = len(rows)
        meta["normalizedSha256"] = transformed_sha
        meta["rawTextPersisted"] = False
        meta["accountIdentifiersPseudonymized"] = True
        provenance["datasets"][dataset] = meta
        print(f"Acquired {dataset}: {len(rows)} normalized structural records")

    (OUT / "provenance.json").write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
