#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from rdflib import Graph, Literal, Namespace, RDF, XSD

ROOT = Path(__file__).resolve().parents[1]
CM = Namespace("https://w3id.org/commentium#")
MAP = Namespace("https://w3id.org/commentium/mapping#")
EX = Namespace("https://example.org/commentium-design-map/")


def load_jsonl(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def q(value):
    return quote(str(value), safe="")


def epoch_literal(value):
    seconds = float(value)
    if seconds > 10**12:
        seconds /= 1000.0
    dt = datetime.fromtimestamp(seconds, tz=timezone.utc).replace(microsecond=0)
    return Literal(dt.isoformat().replace("+00:00", "Z"), datatype=XSD.dateTime)


def bind(g):
    g.bind("cm", CM)
    g.bind("map", MAP)
    g.bind("exmap", EX)


def medium_uri(dataset):
    return EX[f"{dataset}/medium"]


def event_uri(dataset, source_id):
    return EX[f"{dataset}/comment/{q(source_id)}"]


def message_uri(dataset, source_id):
    return EX[f"{dataset}/message/{q(source_id)}"]


def agent_uri(dataset, source_id):
    return EX[f"{dataset}/agent/{q(source_id)}"]


def situation_uri(dataset, source_id):
    return EX[f"{dataset}/situation/{q(source_id)}"]


def thread_uri(dataset, source_id):
    return EX[f"{dataset}/thread/{q(source_id)}"]


def add_comment(g, dataset, source_id, speaker, anchor, timestamp, text, *, response_to=None, thread=None, subject=None):
    event = event_uri(dataset, source_id)
    message = message_uri(dataset, source_id)
    agent = agent_uri(dataset, speaker if speaker not in (None, "") else "opaque")
    situation = situation_uri(dataset, source_id)
    medium = medium_uri(dataset)

    g.add((event, RDF.type, CM.Comment))
    if response_to is not None:
        g.add((event, RDF.type, CM.Response))
        g.add((event, CM.respondsTo, response_to))
    g.add((message, RDF.type, CM.CommentMessage))
    g.add((anchor, RDF.type, CM.Commentable))
    g.add((agent, RDF.type, CM.Agent))
    g.add((agent, RDF.type, CM.Commenter))
    g.add((situation, RDF.type, CM.Situation))
    g.add((medium, RDF.type, CM.Medium))

    g.add((event, CM.hasMessage, message))
    g.add((event, CM.anchoredTo, anchor))
    g.add((event, CM.hasCommenter, agent))
    g.add((event, CM.occursIn, situation))
    g.add((event, CM.via, medium))
    g.add((event, CM.hasTime, epoch_literal(timestamp)))
    if thread is not None:
        g.add((thread, RDF.type, CM.CommentThread))
        g.add((event, CM.partOfThread, thread))
    if subject is not None:
        g.add((subject, RDF.type, CM.CommentSubject))
        g.add((event, CM.isAbout, subject))

    g.add((event, MAP.sourceDataset, Literal(dataset)))
    g.add((event, MAP.sourceRecordId, Literal(str(source_id))))
    g.add((message, MAP.sourceText, Literal(text or "")))
    return event, message


def map_amazon(profile, rows):
    dataset = profile["id"]
    g = Graph(); bind(g)
    for row in rows:
        parent = row.get("parent_asin") or row.get("asin")
        key_raw = f"{row.get('user_id')}|{parent}|{row.get('timestamp')}"
        source_id = hashlib.sha1(key_raw.encode("utf-8")).hexdigest()[:16]
        product = EX[f"{dataset}/product/{q(parent)}"]
        event, message = add_comment(
            g, dataset, source_id, row.get("user_id"), product, row.get("timestamp"),
            (row.get("title") or "") + "\n" + (row.get("text") or ""), subject=product
        )
        g.add((message, MAP.asin, Literal(row.get("asin", ""))))
        g.add((message, MAP.parentAsin, Literal(parent)))
        g.add((event, MAP.rating, Literal(float(row.get("rating")), datatype=XSD.decimal)))
        g.add((event, MAP.verifiedPurchase, Literal(bool(row.get("verified_purchase")), datatype=XSD.boolean)))
        g.add((event, MAP.helpfulVote, Literal(int(row.get("helpful_vote", 0)), datatype=XSD.integer)))
    return g


def map_reddit(profile, rows):
    dataset = profile["id"]
    g = Graph(); bind(g)
    roots = {r["id"] for r in rows if r.get("id") == r.get("conversation_id")}
    row_by_id = {r["id"]: r for r in rows}
    mapped_ids = {r["id"] for r in rows if r["id"] not in roots}

    for root in roots:
        host = EX[f"{dataset}/post/{q(root)}"]
        g.add((host, RDF.type, CM.Commentable))

    for row in rows:
        if row["id"] in roots:
            continue
        host = EX[f"{dataset}/post/{q(row['conversation_id'])}"]
        thread = thread_uri(dataset, row["conversation_id"])
        reply_to = row.get("reply_to")
        predecessor = event_uri(dataset, reply_to) if reply_to in mapped_ids else None
        event, message = add_comment(
            g, dataset, row["id"], row.get("speaker"), host, row.get("timestamp"), row.get("text", ""),
            response_to=predecessor, thread=thread
        )
        meta = row.get("meta") or {}
        if "score" in meta:
            g.add((event, MAP.score, Literal(int(meta["score"]), datatype=XSD.integer)))
        if meta.get("top_level_comment") is not None:
            g.add((event, MAP.topLevelComment, Literal(str(meta["top_level_comment"]))))
    return g


def map_wikiconv(profile, rows):
    dataset = profile["id"]
    g = Graph(); bind(g)
    mapped_rows = [r for r in rows if not (r.get("meta") or {}).get("is_section_header", False)]
    mapped_ids = {r["id"] for r in mapped_rows}

    for row in mapped_rows:
        host = EX[f"{dataset}/host/{q(row['conversation_id'])}"]
        thread = thread_uri(dataset, row["conversation_id"])
        reply_to = row.get("reply_to")
        predecessor = event_uri(dataset, reply_to) if reply_to in mapped_ids else None
        event, message = add_comment(
            g, dataset, row["id"], row.get("speaker"), host, row.get("timestamp"), row.get("text", ""),
            response_to=predecessor, thread=thread
        )
        meta = row.get("meta") or {}
        g.add((event, MAP.actionType, Literal(str(row.get("type", "")))))
        if meta.get("rev_id") is not None:
            g.add((event, MAP.revisionId, Literal(int(meta["rev_id"]), datatype=XSD.integer)))
        if meta.get("toxicity") is not None:
            g.add((event, MAP.toxicityScore, Literal(float(meta["toxicity"]), datatype=XSD.decimal)))
    return g


ADAPTERS = {
    "amazon_reviews_2023": map_amazon,
    "reddit_convokit": map_reddit,
    "wikiconv": map_wikiconv,
}


def main():
    profiles = sorted((ROOT / "mappings" / "design").glob("*.profile.json"))
    summary = {"datasets": {}}
    for profile_path in profiles:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        rows = load_jsonl(ROOT / profile["inputFixture"])
        if not all(bool(r.get("synthetic")) for r in rows):
            raise RuntimeError(f"Committed regression fixture must be explicitly synthetic: {profile_path}")
        adapter = ADAPTERS[profile["adapter"]]
        graph = adapter(profile, rows)
        out = ROOT / profile["output"]
        out.parent.mkdir(parents=True, exist_ok=True)
        graph.serialize(destination=out, format="turtle")
        summary["datasets"][profile["id"]] = {
            "profile": str(profile_path.relative_to(ROOT)),
            "inputRows": len(rows),
            "outputTriples": len(graph),
            "output": profile["output"],
        }
        print(f"Mapped {profile['id']}: {len(rows)} source rows -> {len(graph)} RDF triples")

    summary_path = ROOT / "validation-results" / "mappings" / "mapping-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
