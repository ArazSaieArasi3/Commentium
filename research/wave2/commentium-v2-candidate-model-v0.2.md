# Commentium v2 Candidate Conceptual Model v0.2

Status: candidate after P1 + P2 refinement and whole-model OntoUML review. Not yet canonical OWL.

## Core inventory

The domain-concept count remains **22**. The changes below are stereotype/semantic corrections, not ontology inflation.

| Concept | v1 | v2 candidate v0.2 | Decision |
|---|---|---|---|
| Comment | event | event | keep |
| Response | subkind/event drift | **event**, specialization of Comment | correct |
| CommentThread | collective | **event** (complex conversational event) | correct |
| Commentable | mixin | **historicalRoleMixin** | correct |
| Agent | kind | **category** | correct |
| Commenter | role | **historicalRoleMixin** | correct |
| IntendedAudience | role | **derived roleMixin** | refine |
| CommentSubject | role | **derived roleMixin** | correct |
| ReferencedEntity | role | **derived roleMixin** | correct |
| Interpretation | relator | **event** | correct |
| InterpretedMeaning | information object | information object | keep |
| InterpretiveAssumption | information object | information object | keep |
| AssertedRelation | relator | **information object** | correct |
| AssertedRelationKind | datatype | **enumeration** | correct |
| InteractionNorm | social object | social object | keep |
| Situation | situation | situation | keep |
| Medium | kind | **category** | correct |
| CommentMessage | information object | information object | keep; multimodal/representation-neutral |
| Intent | mode | mode | keep |
| Stance | mode | mode | keep |
| ExpressionStyle | quality | quality | keep; bearer is CommentMessage |
| Time | quality | quality / temporal qualification | keep pending formal implementation |

## Candidate relations and conceptual cardinalities

Important: these are **ontological cardinalities**, not statements about whether a dataset happens to record every value. Missing source data is handled at mapping/provenance level.

| Relation | Domain -> Range | Conceptual cardinality/rule | OntoUML intent |
|---|---|---|---|
| `hasMessage` | Comment -> CommentMessage | Comment exactly 1 semantic message | association/creation semantics to formalize |
| `anchoredTo` | Comment -> Commentable | Comment 1..* anchors | participation |
| `occursIn` | Comment -> Situation | Comment 1..* contextual situations | contextual relation |
| `via` | Comment -> Medium | Comment 1..* communication media | participation/contextual |
| `hasTime` | Comment -> Time | Comment exactly 1 temporal qualification | temporal characterization |
| `hasExpressionStyle` | CommentMessage -> ExpressionStyle | 0..* | characterization |
| `respondsTo` | Response -> Comment | Response 1..* predecessors; profile may narrow to exactly 1 | acyclic directed dependence |
| `partOfThread` | Comment -> CommentThread | 0..* thread-event wholes | participational event decomposition |
| `hasCommenter` | Comment -> Commenter | Comment 1..* authors | participation |
| `addresses` | Comment -> IntendedAudience | 0..* | derived semantic relation |
| `isAbout` | Comment -> CommentSubject | 0..* | derived semantic relation |
| `refersTo` | CommentMessage -> ReferencedEntity | 0..* | derived semantic/content relation |
| `inheresIn` | Intent/Stance -> Agent | each mode exactly 1 bearer | characterization |
| `motivatedBy` | Comment -> Intent | 0..* | intentional dependence |
| `reflects` | Comment -> Stance | 0..* | intentional/evaluative dependence |
| `governedBy` | Situation -> InteractionNorm | 0..* | normative contextual relation |
| `performedBy` | Interpretation -> Agent | 1..* participating interpreters | participation |
| `interpretsMessage` | Interpretation -> CommentMessage | exactly 1 | event-object relation |
| `producesMeaning` | Interpretation -> InterpretedMeaning | 1..* | creation/result relation |
| `basedOn` | Interpretation -> InterpretiveAssumption | 0..* | dependency |
| `groundedIn` | InterpretedMeaning -> InterpretiveAssumption | 0..* | semantic grounding |
| `assertedIn` | AssertedRelation -> CommentMessage | exactly 1 | content-location relation |
| `involvesSubject` | AssertedRelation -> CommentSubject | 0..* | semantic relation |
| `involvesReference` | AssertedRelation -> ReferencedEntity | 0..* | semantic relation |
| `typedAs` | AssertedRelation -> AssertedRelationKind | exactly 1 when materialized | classification |

Constraint: each materialized AssertedRelation must involve at least one subject or one referenced entity.

## Target-semantics separation

The v2 candidate keeps five non-equivalent semantics:

1. `anchoredTo` — structural anchor/host;
2. `respondsTo` — conversational predecessor;
3. `isAbout` — semantic subject;
4. `refersTo` — entity referenced in message content;
5. `addresses` — intended audience/addressee.

## Operational rules

### Unknown author
The existence of an author does not depend on recorded platform identity. A source mapping may instantiate an opaque/local Agent when identity is unavailable.

### Audience inference
Explicit and inferred audiences are not merged. Inferred `addresses` assertions require provenance/confidence metadata in the implementation/profile layer.

### Multimodality
One CommentMessage may have multiple textual/visual/audio/video representations or parts in an alignment/profile layer. No media-specific Core classes are introduced.

### Rating
Raw rating remains source/profile data. Mapping a rating to Stance is a separate interpretation step.

### Lifecycle
Comment/message history is handled with PROV-O-aligned revision/activity/invalidation structures, not Core classes.

## v1 -> v2 breaking conceptual changes

- `Response`: subkind -> event specialization.
- `CommentThread`: collective -> complex event.
- `memberOf` -> `partOfThread` participational event decomposition.
- `Commentable`: mixin -> historicalRoleMixin.
- `Agent`: kind -> category.
- `Commenter`: role -> historicalRoleMixin.
- `CommentSubject`: role -> derived roleMixin; no Agent-only bearer.
- `ReferencedEntity`: role -> derived roleMixin; no Agent-only bearer.
- `Interpretation`: relator -> event.
- `AssertedRelation`: relator -> information object.
- `AssertedRelationKind`: datatype -> enumeration.
- `Medium`: kind -> category.
- `isAboutOrDirectedTo` -> `isAbout`.
- remove conceptual `playedBy` role reification.
- `refersTo` domain corrected to CommentMessage.
- `governedBy` domain clarified to Situation.
- `hasExpressionStyle` bearer moved to CommentMessage.

## Status for Gate C

v0.2 is eligible for formal OntoUML encoding and validator execution. It is **not yet frozen** because the three derived RoleMixins (`IntendedAudience`, `CommentSubject`, `ReferencedEntity`) need a final grounding check in the executable OntoUML representation, and relation stereotypes/cardinalities must be validator-tested.