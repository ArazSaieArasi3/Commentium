# Commentium v2 — Gate C Conceptual Freeze Record

Date: 2026-08-22

Status: **FROZEN FOR IMPLEMENTATION**

## Frozen source

The conceptual source for the v2 implementation block is:

- `research/wave2/commentium-v2-candidate-model-v0.3.md`
- reproducibly generated machine-readable model: `research/wave2/commentium-v2-candidate-v0.3.ontouml.json`
- generator: `scripts/build_commentium_ontouml.mjs`

The generated JSON is a CI/release artifact; the generator plus the frozen decision record are the maintained source until release packaging.

## Gate C evidence

### Current OntoUML exchange/toolchain

Pinned validation toolchain:
- `ontouml-schema` 1.0.2
- `ontouml-js` 1.0.0
- AJV 8.20.0
- AJV Formats 3.0.1

Final CI run used the official/current JSON exchange schema with id:

`https://w3id.org/ontouml/schema/v1.0.2`

Results:
- direct JSON Schema validation: **PASS**
- `ontouml-js` validation: **PASS**
- `ontouml-js` parse/round-trip: **PASS**
- Gate C deterministic semantic/anti-pattern guardrails: **71/71 PASS, 0 FAIL**
- design-dataset regression: **Amazon PASS, Reddit PASS, WikiConv PASS**
- Core concept count: **22**

CI evidence:
- workflow: `OntoUML Verify`
- run id: `32566459324`
- verification artifact id: `9474201089`
- artifact digest: `sha256:68c1d0d312a94fe27711d8b662706fe9fee786039b8ee1775784e7b3b77eaa61`

## OntoUML Server compatibility note

The public OntoUML Server deployment could not be used as a normative Gate C validator for the current exchange format:

- `https://api.ontouml.org/v1/verify`: unavailable from CI;
- `http://api.ontouml.org/v1/verify`: reachable but returned HTTP 400 `The input could not be parse into a valid instance of Project.`;
- documented legacy `:3001` endpoint: unavailable.

The server repository currently represents a legacy stack relative to the pinned current schema/toolchain. Therefore the server parse failure is recorded as a **deployment/toolchain compatibility limitation**, not as evidence of a Commentium model defect. Gate C relies on the current official JSON Schema, current `ontouml-js` validation/round-trip, deterministic semantic checks, catalogue-informed OntoUML review, and design-dataset regressions.

This limitation must be reported transparently in reproducibility documentation; it must not be described as an OntoUML Server validation pass.

## Anti-pattern decisions

### FreeRole-like semantic role views

`IntendedAudience`, `CommentSubject`, and `ReferencedEntity` are retained as **derived RoleMixin views** defined by `addresses`, `isAbout`, and `refersTo` respectively.

Decision:
- do not introduce artificial Relators merely to silence a warning;
- a Relator may be introduced later only if a genuine relational truth-maker is ontologically justified;
- the derived status must remain explicit in conceptual and operational documentation.

### Historical roles

`Commenter` and `Commentable` are historical role mixins grounded in participation in a `Comment` event.

### Event/thread correction

`CommentThread` is frozen as a complex event and `partOfThread` as event decomposition. The v1 `collective/memberOf` pattern is retired for v2.

### Role reification

The v1 `playedBy` role-individual pattern is retired from the conceptual v2 Core.

## Frozen conceptual delta from v1

Key breaking corrections include:
- `Response`: event specialization of `Comment`;
- `CommentThread`: complex event rather than collective;
- `Commentable`: historicalRoleMixin;
- `Agent`: category;
- `Commenter`: historicalRoleMixin;
- `IntendedAudience`, `CommentSubject`, `ReferencedEntity`: derived RoleMixins;
- `Interpretation`: event rather than relator;
- `AssertedRelation`: propositional/information-object semantics rather than relator;
- `AssertedRelationKind`: enumeration;
- `Medium`: category;
- `Time`: datatype/temporal qualification rather than quality;
- remove conceptual `playedBy`;
- replace `memberOf` with `partOfThread`;
- replace `isAboutOrDirectedTo` with `isAbout`;
- correct reference semantics to `CommentMessage -> ReferencedEntity`;
- distinguish structural anchor, reply, aboutness, reference, and audience;
- formally orient OntoUML participation relations Endurant -> Event while allowing domain-friendly inverse properties in OWL/API.

## Freeze rule

From this point, the v0.3 conceptual model is the source of truth for the canonical OWL/SHACL implementation.

No conceptual change is allowed during implementation merely to simplify OWL, SHACL, code, dataset mapping, or tooling. Any proposed conceptual change must:
1. reopen Gate C explicitly;
2. record the evidence that motivates the change;
3. rerun OntoUML/schema/semantic checks;
4. rerun all three design-dataset regressions;
5. produce a new frozen candidate version.

## Release implication

Gate C freeze **does not create a public release**.

The next release milestone remains `v2.0.0-rc.1`, eligible only after the canonical OWL 2 ontology, SHACL constraints, executable competency questions/SPARQL, formal reasoner/validation checks, design mappings, migration documentation, and CI are synchronized and green.
