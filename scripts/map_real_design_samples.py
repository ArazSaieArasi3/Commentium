#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from rdflib import RDF

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import map_design_datasets as mapper

INPUT = ROOT / "validation-results" / "real-samples" / "normalized"
OUTPUT = ROOT / "validation-results" / "real-mappings"
PROFILES = ROOT / "mappings" / "design"


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    summary = {"datasets": {}}
    for profile_path in sorted(PROFILES.glob("*.profile.json")):
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        dataset = profile["id"]
        rows = mapper.load_jsonl(INPUT / f"{dataset}.jsonl")
        if any(bool(r.get("synthetic")) for r in rows):
            raise RuntimeError(f"Real-sample mapper received synthetic rows for {dataset}")
        graph = mapper.ADAPTERS[profile["adapter"]](profile, rows)
        out = OUTPUT / f"{dataset}.ttl"
        graph.serialize(destination=out, format="turtle")
        comments = len(set(graph.subjects(RDF.type, mapper.CM.Comment)))
        responses = len(set(graph.subjects(RDF.type, mapper.CM.Response)))
        summary["datasets"][dataset] = {
            "normalizedInputRows": len(rows), "rdfTriples": len(graph),
            "comments": comments, "responses": responses, "output": str(out.relative_to(ROOT))
        }
        print(f"Mapped real {dataset}: comments={comments}, responses={responses}, triples={len(graph)}")
    (OUTPUT / "mapping-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
