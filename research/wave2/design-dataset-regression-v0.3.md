# Commentium v2 Candidate v0.3 — Design-Dataset Regression

Status: **PASS**. This regression re-checks the frozen-candidate semantics after the v0.3 formal corrections (participation orientation, structural-anchor clarification, and `Time` as a datatype).

## Regression criteria

The v0.3 candidate passes only if the three design families remain representable without:

1. adding platform-specific Core classes;
2. conflating structural anchoring with reply, aboutness, reference, or audience;
3. classifying a prior `Comment` event as a `Commentable` merely because a platform schema calls it a parent comment;
4. forcing subjects/references to be Agents;
5. treating ratings, reactions, moderation labels, provenance, or lifecycle states as intrinsic Core semantics;
6. changing the 22-concept inventory.

## Amazon Reviews 2023

| Phenomenon | v0.3 mapping | Result |
|---|---|---|
| review occurrence | `Comment` event | PASS |
| title/text/images | representations/parts of `CommentMessage` in profile layer | PASS |
| reviewer | `Agent` classified as `Commenter` through authorship participation | PASS |
| reviewed product/resource | persistent resource classified as `Commentable`; conceptual `anchors`, OWL/API inverse `anchoredTo` | PASS |
| semantic evaluated subject | same resource may also satisfy derived `CommentSubject` via `isAbout` | PASS |
| timestamp | `Time` datatype value | PASS |
| Amazon service/channel | `Medium` participating in the Comment occurrence; OWL/API inverse `via` | PASS |
| rating | observed source value; evidence for, but not identical to, `Stance` | PASS |
| helpful vote | feedback/profile extension | PASS boundary |
| verified purchase | provenance/profile extension | PASS boundary |

**Critical regression:** structural anchor and semantic subject may be extensionally the same product while `anchors/anchoredTo` and `isAbout` remain semantically distinct.

**Amazon: PASS.**

## ConvoKit / Reddit

| Phenomenon | v0.3 mapping | Result |
|---|---|---|
| utterance/comment occurrence | `Comment`; `Response` when replying | PASS |
| textual content | `CommentMessage` | PASS |
| speaker | `Agent` classified as `Commenter` | PASS |
| `reply_to` | `Response respondsTo Comment` | PASS |
| conversation grouping | Comment event `partOfThread` complex `CommentThread` event | PASS |
| structural host | persistent post/message/page resource classified as `Commentable`; NOT the prior Comment event merely as an event | PASS |
| semantic subject | derived `CommentSubject` through `isAbout` when established | PASS |
| mentioned entity | `CommentMessage refersTo ReferencedEntity` | PASS |
| inferred addressee | derived `addresses` assertion with provenance/confidence in profile layer | PASS |
| subreddit/community | context/alignment/profile data; no new Core class | PASS boundary |
| score/upvotes | feedback extension/profile | PASS boundary |

**Critical regression:** for a nested reply, `respondsTo` targets the predecessor `Comment` event while structural anchoring targets a persistent resource/message/post according to the mapping profile. No event is forced into the `historicalRoleMixin` `Commentable` merely because of a platform `parent` field.

**Reddit: PASS.**

## WikiConv

| Phenomenon | v0.3 mapping | Result |
|---|---|---|
| talk-page comment | `Comment` / `Response` event | PASS |
| content | `CommentMessage` | PASS |
| author | `Agent` classified as `Commenter` when identifiable; opaque/local Agent when identity unavailable | PASS |
| reply | `respondsTo` prior Comment event | PASS |
| conversation | `partOfThread` `CommentThread` event | PASS |
| Talk Page / persistent host | `Commentable` structural resource participating in Comment event | PASS |
| semantic topic | derived `CommentSubject`, independent of Talk Page anchor | PASS |
| situation/norms | `Situation` and `InteractionNorm` | PASS |
| platform/service | `Medium` | PASS |
| edit/delete/restore | PROV-O-aligned lifecycle extension, not Core | PASS boundary |

**Critical regression:** anchor, reply target, and semantic subject can be three different entities without changing the Core.

**WikiConv: PASS.**

## Cross-dataset result

| Requirement | Amazon | Reddit | WikiConv | Overall |
|---|---:|---:|---:|---|
| 22-concept inventory sufficient | PASS | PASS | PASS | PASS |
| event/message separation preserved | PASS | PASS | PASS | PASS |
| anchor/reply/aboutness/reference/audience distinct | PASS | PASS | PASS | PASS |
| non-Agent subject/reference allowed | PASS | PASS | PASS | PASS |
| CommentThread as complex event works | N/A | PASS | PASS | PASS |
| structural Commentable remains an endurant/resource role | PASS | PASS | PASS | PASS |
| `Time` datatype mapping works | PASS | PASS | PASS | PASS |
| platform-specific signals kept outside Core | PASS | PASS | PASS | PASS |

## Verdict

**3/3 design families PASS after the v0.3 formal corrections.**

No Core class addition is required. The v0.3 corrections do not regress the heterogeneous design-dataset coverage established in v0.1/v0.2.
