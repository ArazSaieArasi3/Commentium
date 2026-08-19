# Commentium v2 Candidate — Design Dataset Stress Test v0.1

Status: completed for the first P1 candidate model using the selected design families. This is a structural/semantic stress test, not the later hold-out generalizability evaluation.

## Pass criteria

The candidate passes a design family only if it can represent the dataset without:
1. collapsing structural anchoring, reply, aboutness, reference, and audience;
2. forcing semantic subjects/references to be Agents;
3. adding platform-specific classes to the Core;
4. treating analytical labels or feedback metrics as intrinsic Core semantics;
5. changing the 22-concept inventory solely to mirror schema fields.

## Dataset A — Amazon Reviews 2023

### Observed structures used in the test
- review rating, title, text and optional images;
- product identifiers (`asin`, `parent_asin`);
- reviewer `user_id`;
- timestamp;
- `verified_purchase`;
- `helpful_vote`;
- product/item metadata.

### Candidate mapping
| Dataset phenomenon | Candidate model mapping | Result |
|---|---|---|
| review occurrence | Comment | PASS |
| title/text/images as review content | CommentMessage | PASS; multimodal representation remains P2 |
| reviewer identity | Agent instantiated contextually as Commenter | PASS |
| reviewed product as structural target | Commentable + `anchoredTo` | PASS |
| product as semantic evaluation subject | same product may instantiate CommentSubject + `isAbout` | PASS; no Agent restriction |
| timestamp | Time | PASS |
| Amazon service/channel | Medium | PASS |
| rating | observed profile value; may provide evidence for Stance but is not equated with Stance | PASS |
| helpful vote | feedback extension/profile | PASS boundary test |
| verified purchase | provenance/profile | PASS boundary test |

### Critical test
The same product can be both a structural anchor and a semantic subject without making `anchoredTo` equivalent to `isAbout`.

**Amazon result: PASS.**

## Dataset B — ConvoKit Reddit

### Observed structures used in the test
ConvoKit utterances provide speaker, conversation identifier, `reply_to`, timestamp and text; Reddit metadata also includes score and top-level-comment information.

### Candidate mapping
| Dataset phenomenon | Candidate model mapping | Result |
|---|---|---|
| Reddit comment/utterance occurrence | Comment or Response | PASS |
| text | CommentMessage | PASS |
| speaker | Agent as Commenter | PASS |
| `reply_to` | Response `respondsTo` Comment | PASS |
| conversation/thread | CommentThread + `memberOf` | PASS |
| parent post/comment as attachment context | Commentable + `anchoredTo` | PASS |
| explicit/implicit topic entity | CommentSubject + `isAbout` when semantically established | PASS |
| mentioned/referred entities | CommentMessage `refersTo` ReferencedEntity | PASS |
| intended addressee inferred from reply or mention | `addresses` IntendedAudience when justified | PASS; inference policy remains P2 |
| subreddit/community | mapping-profile/context metadata, not a new Core class | PASS boundary test |
| score/upvotes | feedback extension/profile | PASS boundary test |
| platform/service | Medium | PASS |

### Critical test
For a nested Reddit reply, `anchoredTo` and `respondsTo` may point to the same parent resource in a particular mapping, but their semantics remain distinct. For a top-level comment, the anchor may be the post while there is no prior Comment response target.

**Reddit result: PASS with P2 caution on inferred audience and unresolved/deleted speaker identity.**

## Dataset C — WikiConv

### Observed structures used in the test
WikiConv represents Wikipedia Talk Page conversational history and explicitly preserves deletion, modification and restoration phenomena.

### Candidate mapping
| Dataset phenomenon | Candidate model mapping | Result |
|---|---|---|
| talk-page comment occurrence | Comment / Response | PASS |
| message content | CommentMessage | PASS |
| author | Agent as Commenter | PASS where identifiable; unresolved identity pattern remains P2 |
| conversational reply structure | `respondsTo` | PASS |
| conversation grouping | CommentThread | PASS |
| talk page / structural resource | Commentable + `anchoredTo` | PASS |
| semantic subject separate from talk page | CommentSubject + `isAbout` | PASS |
| context of occurrence | Situation | PASS |
| Wikipedia service/channel | Medium | PASS |
| interaction norms | Situation `governedBy` InteractionNorm | PASS conceptually |
| deletion/modification/restoration | PROV/lifecycle extension, not Core | PASS boundary test |

### Critical test
A talk-page comment can be anchored on a Talk Page, reply to a prior comment, and be semantically about a third entity. The v2 candidate represents all three without conflation.

**WikiConv result: PASS with P2 caution on lifecycle/provenance operationalization and unidentified actors.**

## Cross-dataset stress matrix

| Requirement | Amazon | Reddit | WikiConv | Overall |
|---|---:|---:|---:|---|
| Comment/event representation | PASS | PASS | PASS | PASS |
| Message separation | PASS | PASS | PASS | PASS |
| Structural anchoring | PASS | PASS | PASS | PASS |
| Reply kept distinct from anchor | N/A | PASS | PASS | PASS |
| Semantic aboutness kept distinct | PASS | PASS | PASS | PASS |
| Non-Agent subject/reference allowed | PASS | PASS | PASS | PASS |
| Thread support without forcing it on reviews | PASS | PASS | PASS | PASS |
| Platform/community fields kept outside Core when appropriate | PASS | PASS | PASS | PASS |
| Feedback/provenance labels prevented from inflating Core | PASS | PASS | PASS | PASS |
| 22-concept inventory sufficient at P1 level | PASS | PASS | PASS | PASS |

## Stress-test verdict

**P1 candidate model: GREEN for the three design families.**

No new Core class is required by this first heterogeneous stress test. The only new Core element supported strongly enough for admission is the `anchoredTo` relation. The strongest conceptual corrections remain:
- `CommentSubject` -> RoleMixin;
- `ReferencedEntity` -> RoleMixin;
- remove Agent-only bearer restrictions;
- remove `playedBy` from the conceptual Core;
- replace `isAboutOrDirectedTo` with `isAbout`;
- correct `refersTo` to CommentMessage -> ReferencedEntity;
- clarify Situation/Medium rather than adding Venue/InteractionSpace.

## What did NOT pass as fully resolved

These are **amber P2 items**, not P1 failures:
1. anonymous/deleted/unresolved authors;
2. explicit versus inferred IntendedAudience;
3. multimodal CommentMessage operationalization;
4. observed rating versus analytic Stance;
5. lifecycle/provenance mapping;
6. full meta-property review of Commentable.

## Decision

Proceed from P1 candidate to **P2 refinement + full OntoUML/constraint stress test**. Do not yet implement the canonical OWL and do not release v2.0.0.