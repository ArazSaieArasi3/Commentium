#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, RDF

ROOT = Path(__file__).resolve().parents[1]
CM = Namespace("https://w3id.org/commentium#")
ONTOLOGY = ROOT / "ontology" / "commentium-v2-candidate.ttl"
SHAPES = ROOT / "validation" / "commentium-v2.shacl.ttl"
MAPPINGS = ROOT / "validation-results" / "real-mappings"
QUERIES = ROOT / "mappings" / "design" / "portable-queries"
OUT = ROOT / "validation-results" / "real-mappings" / "portability-results.json"

QUERY_FILES = {
    "PQ01": "pq01-core-context.rq",
    "PQ02": "pq02-reply-separation.rq",
    "PQ03": "pq03-thread-membership.rq",
    "PQ04": "pq04-aboutness.rq",
    "PQ05": "pq05-no-retired-vocabulary.rq"
}


def qrows(graph, name):
    result = graph.query((QUERIES / QUERY_FILES[name]).read_text(encoding="utf-8"))
    return len(list(result))


def qask(graph, name):
    result = graph.query((QUERIES / QUERY_FILES[name]).read_text(encoding="utf-8"))
    return bool(result.askAnswer)


def main():
    report = {"datasets": {}, "pass": True}
    for dataset in ["amazon-reviews-2023", "reddit-convokit", "wikiconv"]:
        data = MAPPINGS / f"{dataset}.ttl"
        graph = Graph(); graph.parse(ONTOLOGY, format="turtle"); graph.parse(data, format="turtle")
        data_graph = Graph(); data_graph.parse(data, format="turtle")
        comments = len(set(data_graph.subjects(RDF.type, CM.Comment)))
        responses = len(set(data_graph.subjects(RDF.type, CM.Response)))
        conforms, _, shacl_text = validate(
            data_graph=str(data), shacl_graph=str(SHAPES), ont_graph=str(ONTOLOGY),
            inference="none", abort_on_first=False, allow_infos=True, allow_warnings=True
        )
        actual = {"PQ01": qrows(graph, "PQ01"), "PQ02": qrows(graph, "PQ02"), "PQ03": qrows(graph, "PQ03"), "PQ04": qrows(graph, "PQ04"), "PQ05": qask(graph, "PQ05")}

        if dataset == "amazon-reviews-2023":
            checks = {
                "minimumRealComments": comments >= 10,
                "coreContextRows": actual["PQ01"] == comments,
                "noReplySemanticsFabricated": responses == 0 and actual["PQ02"] == 0,
                "noThreadSemanticsFabricated": actual["PQ03"] == 0,
                "directAboutness": actual["PQ04"] == comments,
                "noRetiredVocabulary": actual["PQ05"] is False
            }
        else:
            checks = {
                "minimumRealComments": comments >= 2,
                "nestedReplyPresent": responses >= 1 and actual["PQ02"] == responses,
                "coreContextRows": actual["PQ01"] == comments,
                "threadRows": actual["PQ03"] == comments,
                "aboutnessNotFabricated": actual["PQ04"] == 0,
                "noRetiredVocabulary": actual["PQ05"] is False
            }
        checks["shaclConforms"] = bool(conforms)
        passed = all(checks.values())
        if not passed:
            report["pass"] = False
        ds = {"comments": comments, "responses": responses, "portableQueryResults": actual, "checks": checks, "pass": passed}
        if not conforms:
            ds["shaclReport"] = shacl_text
        report["datasets"][dataset] = ds

    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    sys.exit(main())
