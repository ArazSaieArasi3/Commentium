# Commentium v2 Candidate Conceptual Model v0.1

Status: **candidate only**. This file records the first evidence-driven v2 conceptual model after Wave 2 P1 ontological analysis. It does not modify the canonical v1.0 ontology.

## Design principle

Preserve the 22-concept core unless heterogeneous evidence requires a change. Prefer semantic correction and relation refinement over ontology inflation.

## Concept inventory

| Concept | v1 stereotype | v2 candidate stereotype | Decision |
|---|---|---|---|
| Comment | event | event | keep |
| Response | subkind of Comment | subkind of Comment | keep |
| CommentThread | collective | collective | keep |
| Commentable | mixin | mixin | keep provisionally; review meta-properties later |
| Agent | kind | kind | keep |
| Commenter | role | role | keep; role classifies its bearer directly |
| IntendedAudience | role | role | keep provisionally; P2 review remains open |
| CommentSubject | role | **roleMixin** | change |
| ReferencedEntity | role | **roleMixin** | change |
| Interpretation | relator | relator | keep |
| InterpretedMeaning | information object | information object | keep |
| InterpretiveAssumption | information object | information object | keep |
| AssertedRelation | relator | relator | keep |
| AssertedRelationKind | datatype | datatype | keep |
| InteractionNorm | social object | social object | keep |
| Situation | situation | situation | keep; clarify as occurrence context |
| Medium | kind | kind | keep; narrow to channel/platform/service |
| CommentMessage | information object | information object | keep; representation may include multimodal content |
| Intent | mode | mode | keep |
| Stance | mode | mode | keep; do not equate with raw rating |
| ExpressionStyle | quality | quality | keep |
| Time | quality | quality | keep |

**Core concept count remains 22. No new class is admitted in v0.1.**

## Candidate core relations and provisional cardinalities

Cardinalities below are intentionally conservative and will be tightened only when ontological necessity and cross-dataset evidence agree.

| Relation | Domain | Range | Candidate cardinality / rule | v2 decision |
|---|---|---|---|---|
| `hasMessage` | Comment | CommentMessage | each Comment exactly 1 message object; message may carry multiple representations | keep/refine |
| `anchoredTo` | Comment | Commentable | each Comment 1..* structural anchors | **new core relation** |
| `occursIn` | Comment | Situation | 0..1 explicit situation in an operational profile; conceptual occurrence context may always exist | keep/clarify |
| `via` | Comment | Medium | 0..1 in a given observation/profile | keep/clarify |
| `hasTime` | Comment | Time | 0..1 recorded temporal qualification | keep |
| `hasExpressionStyle` | Comment | ExpressionStyle | 0..* | keep |
| `respondsTo` | Response | Comment | exactly 1 structural conversational predecessor per Response profile | keep; distinct from anchor |
| `memberOf` | Comment | CommentThread | 0..1 primary thread per mapping profile | keep |
| `hasCommenter` | Comment | Commenter | 1..* ontological authors; identity metadata may be unresolved | keep; no role reification |
| `addresses` | Comment | IntendedAudience | 0..* | keep; distinct from subject |
| `isAbout` | Comment | CommentSubject | 0..* | **rename/refine** from `isAboutOrDirectedTo` |
| `inheresIn` | Intent, Stance | Agent | exactly 1 bearer per mode | keep |
| `motivatedBy` | Comment | Intent | 0..* | keep |
| `reflects` | Comment | Stance | 0..* | keep |
| `governedBy` | Situation | InteractionNorm | 0..* | **clarify domain** to contextual situation |
| `mediatesAgent` | Interpretation | Agent | 1..* | keep |
| `interpretsMessage` | Interpretation | CommentMessage | exactly 1 | keep |
| `produces` | Interpretation | InterpretedMeaning | 1..* | keep |
| `basedOn` | Interpretation | InterpretiveAssumption | 0..* | keep |
| `groundedIn` | InterpretedMeaning | InterpretiveAssumption | 0..* | keep |
| `assertedIn` | AssertedRelation | Comment | exactly 1 | keep |
| `involvesSubject` | AssertedRelation | CommentSubject | 0..* | keep |
| `involvesReference` | AssertedRelation | ReferencedEntity | 0..* | keep |
| `refersTo` | CommentMessage | ReferencedEntity | 0..* | **correct operational domain** |
| `typedAs` | AssertedRelation | AssertedRelationKind | exactly 1 when relation typing is materialized | keep |

## Removed/deprecated conceptual pattern

### `playedBy`

The v1 operationalization reifies role instances and links them to an Agent with `playedBy`. The v2 conceptual model removes this pattern. OntoUML roles classify their bearers directly.

Migration implications:
- an Agent may instantiate `Commenter` or `IntendedAudience` contextually;
- heterogeneous bearers may instantiate `CommentSubject` or `ReferencedEntity` as RoleMixins;
- OWL v2 must document backward compatibility and representation migration from v1.

## Five distinct target-like semantics

1. `anchoredTo`: structural host / attachment target.
2. `respondsTo`: conversational predecessor.
3. `isAbout`: semantic subject / aboutness.
4. `refersTo`: referenced entity in message content.
5. `addresses`: intended audience / addressee.

These may coincide in a particular record but MUST NOT be declared semantically equivalent.

## Core versus profile/extension boundaries

Remain outside the v2 Core unless later evidence overturns the decision:
- rating value as an intrinsic Stance value;
- helpfulness, score, reactions and votes;
- verified purchase and business provenance;
- edit/delete/restore lifecycle events;
- moderation acts and toxicity labels;
- sentiment, emotion, aspect and argumentation labels;
- subreddit/forum/community/container taxonomies.

These should be represented through mapping profiles, alignments, provenance, or capability-specific extensions.

## Open P2 items

1. `IntendedAudience` may eventually need broader heterogeneous bearers; keep as Role until targeted analysis.
2. Anonymous/deleted/unresolved actor representation needs an operational pattern.
3. Multimodal `CommentMessage` needs a representation pattern, not necessarily a new core class.
4. Rating versus Stance mapping must be formalized as observed signal versus analytic mode.
5. `Commentable` stereotype must be revisited during the full OntoUML meta-property/anti-pattern pass.

## Freeze status

This v0.1 candidate is eligible for design-dataset stress testing. It is **not** eligible for canonical OWL implementation or release until the stress test passes and the candidate model is explicitly frozen.