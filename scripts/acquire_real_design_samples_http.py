#!/usr/bin/env python3
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests

import acquire_real_design_samples as base

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "mappings" / "design" / "real-sample-manifest.json"
OUT = ROOT / "validation-results" / "real-samples"
NORMALIZED = OUT / "normalized"


def amazon_sample_direct(cfg):
    prefix = "raw_review_"
    if not cfg["config"].startswith(prefix):
        raise ValueError(f"Unsupported Amazon review config: {cfg['config']}")
    category = cfg["config"][len(prefix):]
    url = (
        "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/"
        f"resolve/main/raw/review_categories/{category}.jsonl?download=true"
    )
    target = int(cfg["targetRecords"])
    raw = []
    with requests.get(url, stream=True, timeout=180, allow_redirects=True) as response:
        response.raise_for_status()
        content_length = response.headers.get("Content-Length")
        etag = response.headers.get("ETag")
        last_modified = response.headers.get("Last-Modified")
        final_url = response.url
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            raw.append(json.loads(line))
            if len(raw) >= target:
                break

    if len(raw) < min(10, target):
        raise RuntimeError(f"Amazon Hugging Face stream returned too few rows: {len(raw)}")

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
            "asin": base.stable_hash("amazon-asin", asin),
            "parent_asin": base.stable_hash("amazon-parent", parent),
            "user_id": base.stable_hash("amazon-user", row.get("user_id") or "opaque"),
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
        "source": cfg["source"],
        "config": cfg["config"],
        "split": cfg["split"],
        "sourceUrl": url,
        "resolvedSourceUrl": final_url,
        "sourceRevisionReference": revision,
        "httpContentLength": content_length,
        "httpETag": etag,
        "httpLastModified": last_modified,
        "selectedRecords": len(raw),
        "rawSelectionSha256": base.canonical_sha(raw),
        "selection": "first N JSONL records streamed from the official McAuley-Lab Hugging Face/Xet source; full file not persisted"
    }


def select_nested_conversations_flexible(rows, max_conversations, max_comments, *, wiki=False):
    """Select bounded conversations even when the structural root is not an Utterance.

    ConvoKit corpora may use conversation_id as the persistent thread/post host without
    materializing that host as an utterance. Nested replies are therefore identified by
    reply_to values that resolve to another actual utterance id, independent of root presence.
    """
    groups = defaultdict(list)
    for row in rows:
        groups[str(row["conversation_id"])].append(row)

    selected = []
    selected_groups = 0
    roots_materialized = 0
    for conversation_id in sorted(groups):
        group = groups[conversation_id]
        by_id = {r["id"]: r for r in group}
        root = by_id.get(conversation_id)
        if root is not None:
            roots_materialized += 1

        candidate_comments = [r for r in group if root is None or r["id"] != conversation_id]
        if wiki:
            candidate_comments = [
                r for r in candidate_comments
                if not bool((r.get("meta") or {}).get("is_section_header", False))
            ]
        candidate_ids = {r["id"] for r in candidate_comments}
        nested = next((r for r in candidate_comments if r.get("reply_to") in candidate_ids), None)
        if nested is None:
            continue

        parent = by_id.get(nested["reply_to"])
        chosen = [root] if root is not None else []
        for r in (parent, nested):
            if r is not None and r not in chosen:
                chosen.append(r)

        ordered = sorted(candidate_comments, key=lambda r: ((r.get("timestamp") or 0), r["id"]))
        for r in ordered:
            selected_comment_count = len([x for x in chosen if x is not root])
            if r not in chosen and selected_comment_count < max_comments:
                chosen.append(r)

        selected.extend(chosen)
        selected_groups += 1
        if selected_groups >= max_conversations:
            break

    if selected_groups == 0:
        raise RuntimeError("No conversation with a resolvable nested utterance reply was found in the bounded corpus")
    return selected, selected_groups, roots_materialized


def corpus_sample_flexible(cfg, dataset, *, wiki=False):
    path, source_url, archive_sha = base.download_corpus_zip(cfg["source"])
    corpus_rows = base.read_utterances_from_zip(path, wiki=wiki)
    raw, conversations, roots_materialized = select_nested_conversations_flexible(
        corpus_rows,
        int(cfg["maxConversations"]),
        int(cfg["maxCommentsPerConversation"]),
        wiki=wiki,
    )
    normalized = base.normalize_conversation_rows(dataset, raw, wiki=wiki)
    return normalized, {
        "source": cfg["source"],
        "sourceUrl": source_url,
        "downloadArchiveSha256": archive_sha,
        "corpusUtterancesRead": len(corpus_rows),
        "selectedRecords": len(raw),
        "selectedConversations": conversations,
        "selectedConversationsWithMaterializedRoot": roots_materialized,
        "rawSelectionSha256": base.canonical_sha(raw),
        "selection": "first lexicographically ordered conversations with a resolvable utterance-to-utterance nested reply; structural root utterance not required; bounded by manifest limits"
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

    amazon, amazon_meta = amazon_sample_direct(cfg["datasets"]["amazon-reviews-2023"])
    reddit, reddit_meta = corpus_sample_flexible(
        cfg["datasets"]["reddit-convokit"], "reddit-convokit", wiki=False
    )
    wiki, wiki_meta = corpus_sample_flexible(
        cfg["datasets"]["wikiconv"], "wikiconv", wiki=True
    )

    for dataset, rows, meta in [
        ("amazon-reviews-2023", amazon, amazon_meta),
        ("reddit-convokit", reddit, reddit_meta),
        ("wikiconv", wiki, wiki_meta),
    ]:
        path = NORMALIZED / f"{dataset}.jsonl"
        transformed_sha = base.write_jsonl(path, rows)
        meta["normalizedRecords"] = len(rows)
        meta["normalizedSha256"] = transformed_sha
        meta["rawTextPersisted"] = False
        meta["accountIdentifiersPseudonymized"] = True
        provenance["datasets"][dataset] = meta
        print(f"Acquired {dataset}: {len(rows)} normalized structural records")

    (OUT / "provenance.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
