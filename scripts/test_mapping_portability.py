#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "mappings" / "design" / "portability-manifest.json"
OUT = ROOT / "validation-results" / "mappings" / "portability-results.json"


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ontology = ROOT / "ontology" / "commentium-v2-candidate.ttl"
    shapes = ROOT / "validation" / "commentium-v2.shacl.ttl"
    report = {"datasets": {}, "pass": True}

    for dataset, cfg in manifest["datasets"].items():
        data_path = ROOT / cfg["graph"]
        graph = Graph(); graph.parse(ontology, format="turtle"); graph.parse(data_path, format="turtle")
        conforms, _, shacl_text = validate(
            data_graph=str(data_path), shacl_graph=str(shapes), ont_graph=str(ontology),
            inference="none", abort_on_first=False, allow_infos=True, allow_warnings=True
        )
        ds = {"shaclConforms": bool(conforms), "queries": {}, "pass": bool(conforms)}
        if not conforms:
            ds["shaclReport"] = shacl_text
            report["pass"] = False

        for query in manifest["queries"]:
            expected = cfg["expect"][query["id"]]
            result = graph.query((ROOT / query["path"]).read_text(encoding="utf-8"))
            rec = {"status": expected["status"], "pass": False}
            if query["form"] == "select":
                actual = len(list(result))
                rec.update({"expectedRows": expected["rows"], "actualRows": actual})
                rec["pass"] = actual == expected["rows"]
            else:
                actual = bool(result.askAnswer)
                rec.update({"expected": bool(expected["ask"]), "actual": actual})
                rec["pass"] = actual == bool(expected["ask"])
            ds["queries"][query["id"]] = rec
            if not rec["pass"]:
                ds["pass"] = False
                report["pass"] = False
        report["datasets"][dataset] = ds

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    sys.exit(main())
