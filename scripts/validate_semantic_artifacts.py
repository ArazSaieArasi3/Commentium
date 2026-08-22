#!/usr/bin/env python3
"""Validate Commentium v2 OWL/SHACL artifacts and positive/negative fixtures."""

from pathlib import Path
import json
import sys

from rdflib import Graph
from pyshacl import validate

ONTOLOGY = Path("ontology/commentium-v2-candidate.ttl")
SHAPES = Path("validation/commentium-v2.shacl.ttl")
VALID = Path("validation/examples/valid-core-instance.ttl")
INVALID = Path("validation/examples/invalid-core-instance.ttl")
OUT = Path("validation-results/shacl")
OUT.mkdir(parents=True, exist_ok=True)


def parse(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path, format="turtle")
    return graph


ontology = parse(ONTOLOGY)
shapes = parse(SHAPES)
valid_data = parse(VALID)
invalid_data = parse(INVALID)

summary = {
    "ontologyTriples": len(ontology),
    "shapeTriples": len(shapes),
    "validFixtureTriples": len(valid_data),
    "invalidFixtureTriples": len(invalid_data),
}

valid_conforms, valid_report_graph, valid_report_text = validate(
    data_graph=valid_data,
    shacl_graph=shapes,
    ont_graph=ontology,
    inference="rdfs",
    advanced=True,
    meta_shacl=True,
    abort_on_first=False,
)
summary["validFixtureConforms"] = bool(valid_conforms)
(OUT / "valid-report.txt").write_text(valid_report_text, encoding="utf-8")
valid_report_graph.serialize(OUT / "valid-report.ttl", format="turtle")

invalid_conforms, invalid_report_graph, invalid_report_text = validate(
    data_graph=invalid_data,
    shacl_graph=shapes,
    ont_graph=ontology,
    inference="rdfs",
    advanced=True,
    meta_shacl=True,
    abort_on_first=False,
)
summary["invalidFixtureConforms"] = bool(invalid_conforms)
(OUT / "invalid-report.txt").write_text(invalid_report_text, encoding="utf-8")
invalid_report_graph.serialize(OUT / "invalid-report.ttl", format="turtle")

(OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))

failures = []
if not valid_conforms:
    failures.append("The valid fixture failed SHACL validation.")
if invalid_conforms:
    failures.append("The intentionally invalid fixture unexpectedly conformed.")

if failures:
    for failure in failures:
        print(f"ERROR: {failure}", file=sys.stderr)
    sys.exit(2)

print("Semantic artifact validation: PASS")
