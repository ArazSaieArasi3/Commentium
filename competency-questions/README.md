# Commentium v2 Executable Competency Questions

Status: **implementation regression suite v0.1**

This directory operationalizes competency questions as executable SPARQL contracts against the Gate-C-frozen Commentium v2 OWL candidate.

## Design principles

1. Every CQ is a domain question, not a low-level triple test.
2. Every executable CQ has an explicit expected result in `manifest.json`.
3. The suite runs against a SHACL-conformant regression fixture.
4. The suite covers all **22 frozen Core concepts** at least once.
5. Structural anchoring, reply-event targeting, aboutness, audience, and message reference are tested as separate semantics.
6. Retired v1 vocabulary is guarded by a negative migration regression.
7. Dataset portability is deliberately evaluated later against real Amazon/Reddit/WikiConv mappings; synthetic fixture success is not reported as cross-dataset validation.

## CQ categories

| Category | CQs | Main purpose |
|---|---|---|
| Core structure | CQ01 | Minimum semantic description of a Comment event |
| Conversation | CQ02-CQ03 | Reply and thread semantics |
| Semantic targets | CQ04 | Aboutness, audience, and reference separation |
| Interpretation | CQ05-CQ06 | Interpretive event provenance and assumptions |
| Asserted content | CQ07-CQ08 | Materialized asserted relations and citations |
| Intentional / expression | CQ09-CQ10 | Intent, stance, and expression style |
| Governance | CQ11 | Interaction norms and situations |
| Semantic separation | CQ12, CQ15 | Anchor vs reply-event distinction |
| Integration | CQ13 | Medium/commenter retrieval |
| Migration regression | CQ14 | Absence of retired v1 predicates |

## Core-concept coverage

The manifest requires coverage of all frozen Core concepts:

`Comment`, `Response`, `CommentThread`, `Commentable`, `Agent`, `Commenter`, `IntendedAudience`, `CommentSubject`, `ReferencedEntity`, `Interpretation`, `InterpretedMeaning`, `InterpretiveAssumption`, `AssertedRelation`, `AssertedRelationKind`, `InteractionNorm`, `Situation`, `Medium`, `CommentMessage`, `Intent`, `Stance`, `ExpressionStyle`, and `Time`.

The runner fails if any required Core concept is omitted from the CQ coverage declarations.

## Execution

```bash
python scripts/run_cq_suite.py
```

The runner:
- parses the ontology and CQ regression data;
- confirms the fixture conforms to the v2 SHACL shapes;
- executes every SPARQL query;
- compares SELECT result sets or ASK booleans with explicit expectations;
- checks 22/22 Core-concept coverage;
- writes `validation-results/cq/cq-results.json`;
- exits non-zero on any mismatch.

## Evidence boundary

Passing this suite establishes **executable competency coverage for the canonical v2 candidate on a controlled regression fixture**. It does not by itself establish external generalizability. Cross-dataset CQ portability is evaluated separately using the reproducible design-dataset mappings tracked in Issue #21 and Issue #35.
