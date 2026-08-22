# Commentium v2 Candidate v0.2 — Executable Model Validation v0.1

Status: executable project-level validation completed on the machine-readable OntoUML Vocabulary/Turtle candidate. This is intentionally distinguished from an official OntoUML validator run.

## Artifacts

- `research/wave2/commentium-v2-candidate-v0.2.ontouml.ttl`
- `scripts/validate_ontouml_candidate.py`

## What was executed

1. RDF/Turtle round-trip parsing with `rdflib`.
2. Deterministic validation rules over the OntoUML Vocabulary graph.
3. Checks of the 22-concept inventory, stereotype decisions, generalizations, key relation stereotypes/endpoints, cardinalities, forbidden legacy relations, target-semantics separation, and explicit grounding/defining relations for role-like concepts.

## Result

**55 / 55 project-level executable checks PASS; 0 FAIL.**

The locally generated validation graph round-tripped successfully as Turtle and contained 713 triples in the compact executable representation used by the reproducible validator.

### Passed check groups

- exactly 22 Core classes;
- all Core classes use the approved v0.2 OntoUML stereotype set;
- `Response` is an event specialization of `Comment`;
- `CommentThread` is an event, not a collective;
- `Commentable` and `Commenter` are `historicalRoleMixin`;
- `Agent` and `Medium` are `category`;
- `IntendedAudience`, `CommentSubject`, `ReferencedEntity` are derived `roleMixin` candidates;
- `Interpretation` is an event;
- `AssertedRelation` is represented as an information/propositional object using a valid OntoUML sortal stereotype plus semantic-nature annotation;
- `AssertedRelationKind` is an enumeration with ten literals;
- `anchoredTo`, `via`, `hasCommenter`, `performedBy` use participation where intended;
- `partOfThread` uses participational event decomposition;
- intrinsic styles/modes use characterization directions where specialized OntoUML relations are justified;
- `refersTo` has `CommentMessage` as source;
- `governedBy` has `Situation` as source;
- `assertedIn` points from asserted content to `CommentMessage`;
- legacy `playedBy`, `memberOf`, and `isAboutOrDirectedTo` are absent;
- all five target-like semantics are present and distinct: anchor, reply, aboutness, reference, audience;
- key target cardinalities match the v0.2 candidate decisions.

## Important limitation

The official OntoUML validator package/tooling was **not available in the current execution environment**. The environment had RDF and JSON Schema libraries available, but no installed `ontouml` / `ontouml_validator` package. Therefore this report MUST NOT be described as an official OntoUML validation pass.

The current result is stronger than a manual checklist because the machine-readable model is parsed and tested executablely, but an official-tool/schema/anti-pattern validation remains a Gate C requirement.

## FreeRole-style caution

The three derived semantic role views:
- `IntendedAudience`
- `CommentSubject`
- `ReferencedEntity`

have explicit defining relations in the machine-readable candidate (`addresses`, `isAbout`, `refersTo`). The project validator confirms those definitions are present. However, if an official OntoUML anti-pattern validator still reports a FreeRole warning because these RoleMixins are not mediated by explicit Relators, do not introduce artificial Relators merely to remove a warning.

Preferred decision sequence if such a warning occurs:
1. verify whether the derived-role definition is supported by the validator/profile being used;
2. if not, treat the concepts as derived semantic views/profile classes rather than primary independent role commitments;
3. introduce a Relator only if a genuine truth-making relational entity can be ontologically justified.

## Relation stereotype policy

Not every relation is forced into a specialized OntoUML relation stereotype. Generic associations are retained where no UFO-specific relation stereotype is justified. This is preferable to assigning a semantically incorrect stereotype simply to make the model look more formal.

## Gate C verdict

**AMBER-GREEN / near-ready, but not frozen.**

Completed:
- P1/P2 conceptual decisions;
- heterogeneous design-dataset stress test;
- whole-model catalogue-informed OntoUML/cardinality stress test;
- machine-readable OntoUML Vocabulary/Turtle candidate;
- reproducible executable project validator;
- 55/55 local checks passing.

Remaining blockers before Gate C freeze:
1. run official OntoUML schema/validator and anti-pattern tooling in a reproducible environment/CI;
2. resolve or document any official warnings, especially FreeRole-like warnings;
3. rerun the design-dataset mapping regression after any validator-driven model change;
4. freeze v0.2 (or a corrected v0.3) as the conceptual source for canonical OWL/SHACL generation.

## Release consequence

Do not release `v2.0.0-rc.1` yet. Once Gate C is frozen, the next block is canonical OWL 2 + SHACL + executable CQ/SPARQL + formal reasoner/validation + CI. The first public release candidate is created only after that block is green.