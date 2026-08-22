# Commentium v2 — Executable Competency Question / SPARQL Regression v0.1

Date: 2026-08-22

Status: **GREEN for the controlled Core regression fixture**

## Scope

This work operationalizes Commentium v2 competency questions as executable SPARQL tests against the Gate-C-frozen OWL candidate.

Artifacts:
- `competency-questions/README.md`
- `competency-questions/manifest.json`
- `competency-questions/queries/*.rq`
- `validation/examples/cq-regression-fixture.ttl`
- `scripts/run_cq_suite.py`
- `.github/workflows/cq-regression.yml`

## Test architecture

Each CQ is treated as an executable semantic contract:
1. a domain-level competency question;
2. an explicit SPARQL SELECT or ASK query;
3. declared Core-concept coverage;
4. explicit expected columns/results or expected boolean;
5. machine comparison of actual vs expected results;
6. CI failure on any mismatch.

The regression fixture is itself required to conform to `validation/commentium-v2.shacl.ttl` before the CQ queries are evaluated.

## Coverage

- executable CQs: **15**
- frozen Core concepts required: **22**
- frozen Core concepts covered: **22/22**
- missing Core concepts: **0**

Covered semantic areas include:
- Comment event structure and context;
- Response/predecessor semantics;
- thread participation;
- semantic subject vs intended audience vs referenced entity;
- interpretation provenance and assumptions;
- asserted relations and citation references;
- intent and stance;
- expression style;
- interaction norms;
- structural anchor vs reply-event target separation;
- medium/commenter retrieval;
- retired-v1-vocabulary regression.

## CI result

Final passing workflow:
- workflow: `Competency Questions`
- run id: `32573283844`
- result: **SUCCESS**
- CQ results: **15/15 PASS**
- SHACL-conformant CQ fixture: **true**
- Core concept coverage: **22/22**
- artifact id: `9475884167`
- artifact digest: `sha256:08578f90dfdbf0113ff6ca100d4fe2d48dc892ac9d9942123108b7a3abd58c91`

The same commit also passed:
- `OntoUML Verify`: **SUCCESS**
- `Semantic Artifacts`: **SUCCESS**

Therefore adding the CQ suite introduced no regression in the frozen conceptual model, OWL 2 DL validation, SHACL validation, or HermiT reasoning.

## Defect found and corrected during test construction

The first CQ run produced **14/15 PASS**. CQ13 originally required explicit `rdf:type cm:Comment` when retrieving comments by medium/commenter. The representative `response1` instance was explicitly typed `cm:Response`; its additional Comment typing follows from the OWL subclass axiom and was not materialized because the CQ runner intentionally uses no inference.

Correction:
- CQ13 was rewritten to query the operational properties `cm:via` and `cm:hasCommenter` directly;
- ontology and fixture were not changed;
- no Gate C reopening was required.

This correction makes the operational CQ independent of whether subclass entailments have been materialized by a reasoner.

## Evidence boundary

This result proves executable competency coverage on a controlled, SHACL-conformant regression fixture. It does **not** yet establish cross-dataset CQ portability or external generalizability.

The remaining part of Issue #21 is to execute an appropriate portable subset of these CQs against reproducible Amazon, Reddit, and WikiConv mappings and record support, adaptation cost, unsupported capabilities, and mapping-dependent query differences.

## Release implication

The executable Core CQ requirement in Issue #35 is now satisfied. Release-candidate eligibility still requires reproducible design-dataset mappings, cross-dataset portability evidence, broader quality/serialization work, synchronization audit, and release packaging.
