#!/usr/bin/env python3
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests
from convokit import Corpus, download

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "mappings" / "design" / "real-sample-manifest.json"
OUT = ROOT / "validation-results" / "real-samples"
NORMALIZED = OUT / "normalized"
CACHE = OUT / "convokit-cache"


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


def utterance_record(utt, wiki=False):
    speaker = getattr(getattr(utt, "speaker", None), "id", None) or "opaque"
    meta = dict(getattr(utt, "meta", {}) or {})
    record = {
        "id": str(utt.id),
        "speaker": str(speaker),
        "conversation_id": str(utt.conversation_id),
        "reply_to": None if utt.reply_to is None else str(utt.reply_to),
        "timestamp": utt.timestamp,
        "text": utt.text or "",
        "meta": meta,
    }
    if wiki:
        record["type"] = getattr(utt, "type", None) or meta.get("type") or ""
    return record


def select_nested_conversations(corpus, max_conversations, max_comments, wiki=False):
    groups = defaultdict(list)
    for utt in corpus.iter_utterances():
        groups[str(utt.conversation_id)].append(utterance_record(utt, wiki=wiki))

    selected = []
    selected_groups = 0
    for conversation_id in sorted(groups):
        rows = groups[conversation_id]
        by_id = {r["id"]: r for r in rows}
        root = by_id.get(conversation_id)
        if root is None:
            continue
        candidate_comments = [r for r in rows if r["id"] != conversation_id]
        if wiki:
            candidate_comments = [r for r in candidate_comments if not bool((r.get("meta") or {}).get("is_section_header", False))]
        candidate_ids = {r["id"] for r in candidate_comments}
        nested = next((r for r in candidate_comments if r.get("reply_to") in candidate_ids), None)
        if nested is None:
            continue
        parent = by_id.get(nested["reply_to"])
        chosen = [root]
        must = [parent, nested]
        for r in must:
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
        raise RuntimeError("No conversation with a resolvable nested reply was found in the selected corpus")
    return selected, selected_groups


def normalize_conversation_rows(dataset, raw, wiki=False):
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


def convokit_sample(cfg, dataset, wiki=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = download(cfg["source"], data_dir=str(CACHE))
    corpus = Corpus(filename=path)
    raw, conversations = select_nested_conversations(
        corpus, int(cfg["maxConversations"]), int(cfg["maxCommentsPerConversation"]), wiki=wiki
    )
    normalized = normalize_conversation_rows(dataset, raw, wiki=wiki)
    return normalized, {
        "source": cfg["source"], "downloadPathName": Path(path).name,
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
    reddit, reddit_meta = convokit_sample(cfg["datasets"]["reddit-convokit"], "reddit-convokit", wiki=False)
    wiki, wiki_meta = convokit_sample(cfg["datasets"]["wikiconv"], "wikiconv", wiki=True)

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
