# Commentium v1.0 Core Coverage Matrix — Wave 2 v0.1

This matrix compares the current 22-concept Core against the structural phenomena visible in the selected design datasets. `D` = directly observable/mappable, `I` = inferable/derived, `N` = not natively present or not needed for the dataset schema.

| Current concept | Amazon Reviews 2023 | ConvoKit Reddit | WikiConv | Wave 2 note |
|---|---:|---:|---:|---|
| Comment | D | D | D | Stable foundational event candidate |
| Response | N | D | D | Strong across conversational datasets |
| CommentThread | N | D | D | Stable for conversational environments; optional in review settings |
| Commentable | D | D | D | Important, but needs an explicit anchoring relation from Comment |
| Agent | D | D | D | Identity metadata may be missing/deleted in some platforms |
| Commenter | D | D | D | Stable contextual role |
| IntendedAudience | N/I | I | I | Often inferred rather than explicitly stored |
| CommentSubject | D | I | I | Must remain distinct from structural host/anchor |
| ReferencedEntity | I | I | I | Usually extracted from message rather than schema-native |
| Interpretation | I | I | I | Analytical layer, intentionally non-observed |
| InterpretedMeaning | I | I | I | Analytical layer |
| InterpretiveAssumption | I | I | I | Analytical/contextual layer |
| AssertedRelation | I | I | I | Derived from semantic content |
| AssertedRelationKind | I | I | I | Controlled analytical classification |
| InteractionNorm | N/I | I | I/D | WikiConv moderation context gives stronger evidence |
| Situation | I | D/I | D/I | Needs clearer operational boundary versus venue/community |
| Medium | D | D | D | Stable at platform/channel level |
| CommentMessage | D | D | D | Needs multimodal-friendly operationalization |
| Intent | I | I | I | Analytical mode |
| Stance | D/I | I | I | Amazon rating is observed signal; stance itself should not be equated with rating |
| ExpressionStyle | I | I | I | Analytical/descriptive quality |
| Time | D | D | D | Stable |

## Initial interpretation

1. The existing 22-concept Core is structurally resilient: all three design families can be expressed without immediately requiring a large number of new classes.
2. The largest pressure is relational rather than class-centric: structural anchoring/hosting is not sufficiently explicit in the public v1.0 relation set.
3. Several v1.0 concepts are intentionally analytical (`Interpretation`, `InterpretedMeaning`, `Intent`, `Stance`, etc.); lack of direct dataset fields is not evidence against them.
4. Dataset discovery currently supports **refinement-first**, not ontology inflation.
5. Candidate additions should therefore be admitted only after UFO/OntoUML analysis and standards comparison.

## Candidate change queue

### P1 — Core-level analysis
- Explicit `Comment -> Commentable` structural anchoring relation.
- Formal distinction among structural anchor, semantic subject, and reply target.
- Medium versus venue/community/situation boundary.

### P2 — Core refinements
- Anonymous/deleted/unresolved actor handling.
- Inferred versus explicitly declared intended audience.
- Multimodal CommentMessage support.
- Observed rating signal versus interpreted Stance.

### P3 — Keep outside Core unless later evidence changes the decision
- Votes/reactions/helpfulness.
- Content lifecycle/provenance.
- Moderation actions and toxicity.
- Sentiment/emotion/aspect/argumentation labels.
- Purchase-verification and other platform/business provenance.