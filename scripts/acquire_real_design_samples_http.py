#!/usr/bin/env python3
import json
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
    reddit, reddit_meta = base.corpus_sample(
        cfg["datasets"]["reddit-convokit"], "reddit-convokit", wiki=False
    )
    wiki, wiki_meta = base.corpus_sample(
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
