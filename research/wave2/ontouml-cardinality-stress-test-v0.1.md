# Commentium v2 Candidate v0.2 — OntoUML & Cardinality Stress Test v0.1

Status: manual/catalogue-informed whole-model stress test before executable OntoUML validation. This report does not claim that an OntoUML validator has already been run on a machine-readable `.ontouml` model.

## Reference basis

The stress test uses the current OntoUML vocabulary/meta-property definitions and the OntoUML anti-pattern catalogue as the conceptual basis. Key principles include:
- `subkind` is a rigid specialization of an identity provider, not an event subtype;
- `category` is rigid and non-sortal across heterogeneous identity principles;
- `roleMixin` is anti-rigid and relationally dependent across heterogeneous identity principles;
- `historicalRoleMixin` captures heterogeneous endurants classified because of participation in an event;
- `memberOf` is object/collective parthood;
- `participational` is event decomposition;
- a Relator is a truth-maker of material relations.

## Whole-model findings

| Check | v0.1 risk | v0.2 action | Verdict |
|---|---|---|---|
| Event specialization | Response as `subkind` | Response -> `event` specialization of Comment | PASS |
| Thread/member ontological nature | Comment event `memberOf` collective Thread | Thread -> complex `event`; use `participational` decomposition | PASS |
| Heterogeneous Agent identity | Agent as `kind` | Agent -> `category` | PASS |
| Heterogeneous author role | Commenter as `role` under broad Agent | Commenter -> `historicalRoleMixin` | PASS |
| Commentable rigidity/dependence | Commentable as capability-like `mixin` | Commentable -> `historicalRoleMixin`, grounded by anchoring participation | PASS |
| Subject/reference heterogeneity | Agent-only role bearers | derived RoleMixins, no Agent-only range | PASS conceptually / AMBER validator grounding |
| Intended audience heterogeneity | Agent-only Role | derived RoleMixin, explicit/inferred distinction | PASS conceptually / AMBER validator grounding |
| Relator semantics: Interpretation | process-like Relator | Interpretation -> Event | PASS |
| Relator semantics: AssertedRelation | asserted content modeled as truth-maker | AssertedRelation -> Information Object | PASS |
| Controlled vocabulary | AssertedRelationKind datatype | enumeration | PASS |
| Medium identity | heterogeneous platform/channel as kind | Medium -> category | PASS |
| Style bearer | quality attached to Comment event | characterize CommentMessage | PASS |
| Role reification | `playedBy` role individuals | remove from conceptual v2 | PASS |

## Anti-pattern catalogue-oriented review

The table focuses on patterns materially relevant to Commentium; catalogue items irrelevant to the current model are marked N/A rather than artificially "passed".

| Anti-pattern family | Assessment | Result |
|---|---|---|
| FreeRole | Commenter/Commentable are grounded through historical participation. IntendedAudience/CommentSubject/ReferencedEntity are derived RoleMixins but their strict tool-level grounding still needs executable validation. | AMBER |
| GSRig / rigidity mismatch | Agent/Medium/Commentable stereotype corrections remove the strongest rigidity mismatches. | PASS |
| MixIden / identity mixing | Agent is now Category; heterogeneous target/reference roles are RoleMixins. | PASS |
| MixRig / rigidity mixing | Commentable no longer modeled as semi-rigid Mixin. | PASS |
| HetColl / HomoFunc | CommentThread is no longer treated as a Collective of event members. | PASS |
| PartOver / WholeOver | Invalid event-to-collective `memberOf` removed; thread relation becomes event decomposition. | PASS |
| Relator-related families (RelComp/RelOver/RelRig/RelSpec/RepRel) | Two constructs previously called Relators were reclassified because their semantics did not match material-relator truth-maker commitments. | PASS at current scope |
| UndefFormal | Several semantic relations still need explicit OntoUML relation stereotypes in the machine-readable model. | AMBER |
| BinOver / DecInt / DepPhase / UndefPhase | No phase/generalization partition structures relevant to these patterns in current Core. | N/A |
| MultDep | No contradictory mandatory dependence paths identified in the candidate relation table. | PASS manual |

## Cardinality review — principle

v0.1 mixed ontological existence with source-data observability. v0.2 separates them.

Example: an anonymous Comment still has an author even if the source has no resolvable user identifier. Therefore `hasCommenter` can remain mandatory conceptually while the mapping records an opaque/unresolved Agent.

## Cardinality stress table

| Relation | v0.2 cardinality | Amazon | Reddit | WikiConv | Verdict |
|---|---|---:|---:|---:|---|
| Comment -> hasMessage | exactly 1 | PASS | PASS | PASS | PASS |
| Comment -> anchoredTo | 1..* | product | post/comment context | talk-page/resource context | PASS |
| Comment -> occursIn | 1..* conceptual | contextual instance can be constructed | contextual instance | contextual instance | PASS |
| Comment -> via Medium | 1..* | Amazon service | Reddit service | Wikipedia service | PASS |
| Comment -> hasTime | exactly 1 ontological temporal qualification | timestamp available | timestamp available | temporal/history data available | PASS |
| Comment -> hasCommenter | 1..* | reviewer | speaker | author/opaque author | PASS with unresolved identity pattern |
| Response -> respondsTo | 1..* | N/A | one parent in profile | reply predecessor(s) | PASS; profile narrows to 1 |
| Comment -> partOfThread | 0..* | no thread required | conversation/thread | talk conversation | PASS |
| Comment -> addresses | 0..* | optional/inferred | optional/inferred | optional/inferred | PASS |
| Comment -> isAbout | 0..* | product commonly | optional topic/entity | optional topic/entity | PASS |
| Message -> refersTo | 0..* | extracted references | mentions/entities | references/entities | PASS |
| Situation -> governedBy Norm | 0..* | optional | community norms | moderation/talk norms | PASS |
| Interpretation -> producesMeaning | 1..* when Interpretation instantiated | analytic layer | analytic layer | analytic layer | PASS |
| AssertedRelation -> typedAs | exactly 1 when materialized | analytic layer | analytic layer | analytic layer | PASS |

## Reply graph constraints

- C4 remains: no Response may respond to itself.
- C5 remains: direct/indirect `respondsTo` cycles are prohibited.
- A Response can have 1..* semantic/conversational predecessors in the Core, while tree-shaped platform profiles may constrain it to exactly one parent.
- `anchoredTo` and `respondsTo` are not equivalent even if a dataset maps both to the same parent resource in a particular record.

## AssertedRelation constraints

- an AssertedRelation is semantic content, not a real-world relation truth-maker;
- it must be asserted in exactly one CommentMessage representation/context when materialized;
- C1: at least one of `involvesSubject` or `involvesReference` must hold;
- controlled kind is singular per AssertedRelation instance; multiple semantic predicates should be represented as multiple asserted relation objects when necessary.

## Regression against design datasets

The P2 corrections do not invalidate the Wave 2 design-dataset PASS:
- Amazon remains mappable without Core classes for rating/helpfulness/verification;
- Reddit remains mappable while separating thread-event membership, anchor, reply, audience and aboutness;
- WikiConv remains mappable while lifecycle is delegated to PROV-O alignment.

## New critical corrections discovered by formal stress

The stress test found five changes that were not merely P2 implementation details:
1. Response -> Event specialization.
2. CommentThread -> complex Event; `memberOf` -> participational `partOfThread`.
3. Agent -> Category and Commenter -> historicalRoleMixin.
4. Interpretation -> Event.
5. AssertedRelation -> Information Object; AssertedRelationKind -> Enumeration.

These are preferred because they make the ontology's stereotypes match the semantics already intended by Commentium rather than adding domain concepts.

## Gate C readiness verdict

**Overall: AMBER-GREEN.**

What is green:
- design-dataset structural coverage;
- main stereotype corrections;
- cardinality architecture;
- thread/reply/anchor distinction;
- no Core-class inflation;
- lifecycle, rating and multimodality boundaries.

Remaining Gate C blockers:
1. create a machine-readable OntoUML v0.2 model;
2. assign exact OntoUML stereotypes to all relations;
3. run executable validator/anti-pattern checks;
4. resolve or explicitly justify any FreeRole warning for `IntendedAudience`, `CommentSubject`, and `ReferencedEntity`;
5. rerun dataset/cardinality checks from the machine-readable model.

Therefore: **do not freeze Gate C and do not build canonical OWL yet.** The immediate next step is formal OntoUML encoding + executable validation of v0.2.