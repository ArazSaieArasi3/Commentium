#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "competency-questions" / "manifest.json"
OUT_DIR = ROOT / "validation-results" / "cq"
OUT_PATH = OUT_DIR / "cq-results.json"


def normalize_term(term):
    if term is None:
        return None
    return str(term)


def sorted_rows(rows):
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=False, ensure_ascii=False))


def main():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    ontology_path = ROOT / manifest["ontology"]
    data_path = ROOT / manifest["data"]
    shapes_path = ROOT / manifest["shapes"]

    graph = Graph()
    graph.parse(ontology_path, format="turtle")
    graph.parse(data_path, format="turtle")

    conforms, _, shacl_text = validate(
        data_graph=str(data_path),
        shacl_graph=str(shapes_path),
        ont_graph=str(ontology_path),
        inference="none",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )

    results = {
        "suiteVersion": manifest["suiteVersion"],
        "ontology": manifest["ontology"],
        "data": manifest["data"],
        "fixtureConformsToShacl": bool(conforms),
        "coreCoverage": {},
        "queries": [],
        "pass": True,
    }

    if not conforms:
        results["pass"] = False
        results["shaclReport"] = shacl_text

    covered = set()
    for cq in manifest["queries"]:
        covered.update(cq.get("covers", []))

    required = set(manifest["requiredCoreConcepts"])
    missing = sorted(required - covered)
    extra = sorted(covered - required)
    results["coreCoverage"] = {
        "required": len(required),
        "covered": len(required - set(missing)),
        "missing": missing,
        "extraDeclarations": extra,
        "pass": not missing,
    }
    if missing:
        results["pass"] = False

    for cq in manifest["queries"]:
        query_path = ROOT / cq["path"]
        record = {
            "id": cq["id"],
            "question": cq["question"],
            "category": cq["category"],
            "query": cq["path"],
            "form": cq["form"],
            "pass": False,
        }
        try:
            query_text = query_path.read_text(encoding="utf-8")
            query_result = graph.query(query_text)

            if cq["form"] == "ask":
                actual = bool(query_result.askAnswer)
                record["expected"] = bool(cq["expected"])
                record["actual"] = actual
                record["pass"] = actual == bool(cq["expected"])
            elif cq["form"] == "select":
                columns = [str(v) for v in query_result.vars]
                actual_rows = [[normalize_term(value) for value in row] for row in query_result]
                expected_rows = cq["expectedRows"]
                record["expectedColumns"] = cq["expectedColumns"]
                record["actualColumns"] = columns
                record["expectedRows"] = expected_rows
                record["actualRows"] = actual_rows
                record["pass"] = (
                    columns == cq["expectedColumns"]
                    and sorted_rows(actual_rows) == sorted_rows(expected_rows)
                )
            else:
                raise ValueError(f"Unsupported query form: {cq['form']}")
        except Exception as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"
            record["pass"] = False

        if not record["pass"]:
            results["pass"] = False
        results["queries"].append(record)

    results["summary"] = {
        "total": len(results["queries"]),
        "passed": sum(1 for q in results["queries"] if q["pass"]),
        "failed": sum(1 for q in results["queries"] if not q["pass"]),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "fixtureConformsToShacl": results["fixtureConformsToShacl"],
        "coreConceptCoverage": f"{results['coreCoverage']['covered']}/{results['coreCoverage']['required']}",
        "queries": results["summary"],
        "pass": results["pass"],
    }, indent=2))

    return 0 if results["pass"] else 2


if __name__ == "__main__":
    sys.exit(main())
