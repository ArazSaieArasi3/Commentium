# Commentium Journal Extension — Evidence Registry v0.1

Status: provisional. This registry records observations before any v2 Core change.

Legend: **Covered** = current construct appears sufficient; **Refine** = current construct/relation may need clarification or formal strengthening; **Candidate** = possible new Core construct/relation; **Extension** = useful but should remain outside Core unless stronger evidence emerges; **Alignment** = prefer reuse/mapping to an external vocabulary.

| ID | Observed phenomenon | Evidence families | Current Commentium coverage | Provisional disposition | Key question |
|---|---|---|---|---|---|
| E01 | Authored communicative occurrence with separable content | Amazon, Reddit, WikiConv | Comment + CommentMessage + Commenter/Agent | Covered | Preserve event/message separation |
| E02 | Explicit reply to an earlier communicative unit | Reddit, WikiConv | Response + respondsTo | Covered/Refine | Ensure reply semantics are not conflated with comment-on-host semantics |
| E03 | Thread/conversation membership | Reddit, WikiConv | CommentThread + memberOf | Covered/Refine | Test roots, nested replies and thread identity criteria |
| E04 | Structural host/anchor on which a comment is posted | Amazon item, Reddit post/comment, Stack Exchange post, article context | Commentable exists but no explicit general host relation is documented or present in the current OWL | **High-priority Candidate relation** | Distinguish structural target/anchor from semantic subject/aboutness |
| E05 | Semantic subject/aboutness may differ from structural host | Reviews and conversational comments | CommentSubject + isAboutOrDirectedTo | Refine | Clarify aboutness versus attachment/hosting/direct-reply |
| E06 | Explicitly referenced entity inside message content | Cross-platform | ReferencedEntity + refersTo/asserted relation machinery | Covered/Refine | Validate direct and indirect references |
| E07 | Platform versus local venue/community/container | Reddit subreddit, Wiki talk context, publisher/site, Amazon marketplace/category | Medium + Situation may partially cover | **Candidate refinement** | Is a reusable InteractionSpace/Community/Container concept needed, or should this be Situation/alignment only? |
| E08 | Social/evaluative feedback on a comment/review | Amazon helpful vote, Reddit score, Stack Exchange score/votes | No explicit comment-feedback event in v1 Core | Extension candidate | Is feedback part of comment semantics or a neighboring interaction module? |
| E09 | Rating/evaluation signal associated with review | Amazon | Stance plus ratingValue-style data mapping | Refine/Extension | Separate observed rating signal from inferred stance |
| E10 | Comment lifecycle: modification, deletion, restoration | WikiConv; Stack Exchange history | Not explicitly modeled | Alignment/Extension | Prefer PROV-O/lifecycle extension rather than Core expansion unless required by invariant comment identity |
| E11 | Moderation action/state and toxicity annotations | WikiConv, Civil Comments | InteractionNorm covers normative context, not moderation acts/labels | Extension | Separate norms, moderation actions and analytical labels |
| E12 | Multimodal message attachments | Amazon review images; ActivityStreams/Web Annotation analogues | CommentMessage currently text-oriented operationally | Refine/Alignment | Should CommentMessage allow multiple content representations/attachments without adding Core classes? |
| E13 | Provenance/verification such as verified purchase | Amazon | Situation/assumptions only indirectly | Alignment/Extension | Model as provenance/evidence rather than intrinsic comment semantics |
| E14 | Missing/deleted/anonymous author identifiers while comment persists | Reddit/Stack Exchange/Civil Comments | Agent/Commenter role structure | Refine | Preserve authorship role without requiring persistent identifiable Agent metadata |
| E15 | Different actor may modify/remove content after original creation | WikiConv/Stack Exchange | No lifecycle-agent model | Alignment/Extension | Provenance activities should distinguish original author from later editors/moderators |
| E16 | Intended audience may be explicit, inferred from reply target, or unknown | Social/Q&A | IntendedAudience | Refine | Avoid requiring explicit audience where only inference exists |
| E17 | Comment target can itself be a comment, post, item, article or other resource | All families | Commentable mixin conceptually supports heterogeneity | Refine | Formalize target range without platform-specific subclasses in Core |
| E18 | Venue/community norms vary while core comment structure remains stable | Reddit/Wiki/publication contexts | Situation + InteractionNorm | Covered/Refine | Strengthen relation between situation/venue and governing norm |
| E19 | A semantic subject or referenced entity may be non-agent (product, article, organization, artifact, place, etc.) | Amazon and cross-platform comment scenarios | Current OWL constrains CommentSubject and ReferencedEntity through `playedBy` whose range is Agent | **High-priority conceptual/formal issue** | Should these roles be borne by a broader entity type/Commentable, or should role modeling be redesigned? |

## Strongest Wave 2 findings so far

### 1. Structural anchoring is missing as an explicit relation
The model must distinguish:
1. **Structural anchoring/hosting** — the resource or container on which the comment is attached/published.
2. **Reply relation** — the prior communicative unit being responded to.
3. **Semantic aboutness/direction** — the entity the comment is about or directed toward.

These can coincide in simple reviews but diverge in social media and Q&A. Commentium v1.0 already has constructs for reply and semantic subject, plus `Commentable` as a mixin, but the current OWL contains no general Comment→Commentable anchoring property.

### 2. Subject/reference role bearers are currently too narrow in OWL
`CommentSubject` and `ReferencedEntity` are described as roles played by an entity, but their OWL restrictions use `playedBy`, whose range is `Agent`. This conflicts with the intended generality of Commentium when the subject/reference is a product, article, post, organization or other non-agent entity. The issue may require a conceptual correction, not merely an OWL patch.

## External-standard pressure

- W3C Web Annotation already provides a Body/Target pattern useful for structural anchoring and should be treated as an interoperability benchmark.
- ActivityStreams provides actor/object/target/context/audience and reply-oriented properties; reuse/alignment should be preferred where semantic commitments match.
- SIOC provides Item/Post/Container/Forum structures useful for community/container alignment.
- PROV-O is a better candidate than Core proliferation for edit/delete/restore provenance.

## Provisional Core-change pressure

### P1 — conceptual/formal analysis before any implementation
- Add or formalize a general structural anchoring relation between Comment and Commentable.
- Clarify structural target versus CommentSubject versus respondsTo.
- Revisit the bearer type of CommentSubject and ReferencedEntity; do not assume all subjects/references are Agents.
- Clarify operational meaning of Medium versus Situation/venue.

### P2 — likely Core refinements
- Make author/audience identification robust to missing or deleted platform identities.
- Generalize CommentMessage operationalization beyond text-only assumptions.
- Separate observed rating signals from inferred Stance.

### P3 — likely extensions/alignment rather than Core
- Reactions/helpfulness/votes
- Moderation actions and toxicity labels
- Sentiment/emotion/aspect
- Argumentation/persuasion
- Edit/delete/restore provenance
- Verified-purchase/evidence metadata

## Next analysis
Run P1 candidates through UFO/OntoUML and standards comparison before changing the ontology. For structural anchoring, test whether the correct solution is (a) a direct material/formal relation to existing Commentable, (b) a contextual target role, or (c) a relator-mediated pattern. For subject/reference roles, determine the correct bearer abstraction and whether `Commentable` is sufficient or a broader entity category is required.