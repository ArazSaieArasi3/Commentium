# Commentium Journal Extension — P1 Ontological Analysis v0.1

Status: preferred decisions for the v2 candidate model; no change has yet been merged into the canonical ontology.

## Decision summary

| ID | Question | Preferred decision | Status |
|---|---|---|---|
| P1.1 | How should structural anchoring be represented? | Add `anchoredTo` from `Comment` to existing `Commentable`; model it as an OntoUML participation relation. Do not add a relator. | ACCEPT for v2 candidate |
| P1.2 | Should anchoring, reply and semantic aboutness remain separate? | Yes. Keep three distinct relations: `anchoredTo`, `respondsTo`, and semantic `isAbout`. | ACCEPT |
| P1.3 | What to do with `isAboutOrDirectedTo`? | Replace with `isAbout`. Direction toward addressees remains represented by `addresses` / `IntendedAudience`. | ACCEPT |
| P1.4 | Can `CommentSubject` be a Role restricted to Agent? | No. Change conceptual stereotype to `RoleMixin`; remove Agent-only bearer restriction. | ACCEPT |
| P1.5 | Can `ReferencedEntity` be a Role restricted to Agent? | No. Change conceptual stereotype to `RoleMixin`; remove Agent-only bearer restriction. | ACCEPT |
| P1.6 | Should role instances be reified through `playedBy` in the conceptual core? | No. Roles should classify their bearers. Remove `playedBy` from the v2 conceptual core and redesign OWL operationalization accordingly. | ACCEPT for conceptual v2; migration strategy required |
| P1.7 | Is a new `InteractionSpace`/`Venue` class required? | Not yet. Do not add one to Core. Clarify `Medium` and `Situation`; map stable containers/communities through external standards and mapping profiles. | DEFER new class; ACCEPT clarification |
| P1.8 | Should `Medium` be redefined? | Keep the concept but narrow its semantics to communication channel/platform/service. It must not stand for subreddit/forum/thread/container. | ACCEPT |
| P1.9 | What is `Situation`? | The contextual situation of the comment occurrence; norms govern the situation. Stable venue/container identity is not a Situation. | ACCEPT |
| P1.10 | What is the correct domain of `refersTo`? | `CommentMessage -> ReferencedEntity`. Keep `involvesReference` for `AssertedRelation -> ReferencedEntity`. | ACCEPT; current OWL drift/defect |
| P1.11 | Should `Commentable` be replaced or re-stereotyped now? | No. Keep the existing `Commentable «mixin»` provisionally to minimize ontology inflation and breaking change; re-evaluate its meta-properties during the full v2 OntoUML anti-pattern pass. | KEEP / REVIEW LATER |

## 1. Structural anchoring

### Problem
Commentium v1.0 has `Commentable` but no general relation connecting a `Comment` to the resource/container on which the comment is structurally attached. Platform schemas repeatedly require this relation.

### Preferred model
`Comment [1] --anchoredTo--> [1..*] Commentable`

Conceptual stereotype for the association: **participation**.

Rationale:
- `Comment` is an event in Commentium.
- OntoUML participation is intended for dependence of an event on an object participating in the event.
- The structural anchor is an object/resource involved in the commenting occurrence.
- No independent truth-maker is needed beyond the commenting event, so introducing a relator would over-model the phenomenon.

Profile-specific mappings may tighten cardinality to exactly one anchor, but Core should allow one or more anchors.

### Interoperability
Candidate mapping:
- Commentium `anchoredTo` ~ W3C Web Annotation `oa:hasTarget` at the structural-target level.
- SIOC `sioc:has_container` is a useful narrower/container-oriented mapping pattern, not a global equivalence.

## 2. Five-way separation of target semantics

The v2 candidate should explicitly distinguish:

1. `anchoredTo` — structural host/anchor.
2. `respondsTo` — conversational predecessor.
3. `isAbout` — semantic subject/aboutness.
4. `refersTo` — entity explicitly/implicitly referenced in the message representation.
5. `addresses` — intended audience/addressee.

These relations may point to the same real-world entity in simple cases but are not semantically equivalent.

### Consequence
Deprecate/replace `isAboutOrDirectedTo` with `isAbout` because `directedTo` overlaps the existing `addresses` relation and obscures the subject/audience distinction.

## 3. CommentSubject

### Problem
The current OWL represents `CommentSubject` as a role whose `playedBy` restriction points to `Agent`. This excludes products, documents, services, places, posts and other non-agent subjects.

### Preferred conceptual decision
`CommentSubject` becomes **«RoleMixin»**.

Rationale:
- being the subject of a comment is anti-rigid and relationally dependent;
- possible bearers follow heterogeneous identity principles;
- OntoUML RoleMixin is the appropriate pattern for relational roles spanning multiple identity providers.

### OWL direction
Do not create a separate role individual connected by `playedBy`. The actual resource can be classified as `CommentSubject` in the relevant representation/profile. Avoid an Agent-only range.

## 4. ReferencedEntity

### Problem
The same Agent-only role issue affects `ReferencedEntity`. Additionally, the current OWL defines `refersTo` with `AssertedRelation` as domain, while the public conceptual relation table intends message-level reference.

### Preferred conceptual decision
`ReferencedEntity` becomes **«RoleMixin»**.

Preferred relations:
- `CommentMessage --refersTo--> ReferencedEntity`
- `AssertedRelation --involvesReference--> ReferencedEntity`

Do not duplicate these semantics.

## 5. Role operationalization cleanup

### Problem
Current OWL creates individuals such as `Commenter` and links them to an `Agent` via `playedBy`. This reifies a role as a separate individual even though the conceptual model labels it as an OntoUML Role.

### Preferred v2 direction
In the conceptual model, roles classify their bearers rather than becoming separate role objects.

Immediate implications:
- `Commenter` remains a Role constrained to Agent-like identity providers.
- `CommentSubject` and `ReferencedEntity` become RoleMixins.
- `playedBy` should not be a core conceptual relation in v2.
- `IntendedAudience` requires a dedicated P2 review because audiences can include persons, organizations, groups or broader populations depending on the profile.

The OWL migration must preserve backward compatibility notes and explicitly document the v1 -> v2 representation change.

## 6. Medium, Situation and venue/container

### Current ambiguity
The current definition of `Medium` permits it to be read as medium, platform or local interaction venue. Dataset evidence distinguishes these notions.

### Preferred decision
Do **not** add `InteractionSpace`, `Community`, `Forum`, or `Venue` to the Core at this stage.

Use the following semantics:
- `Medium`: communication channel/platform/service used to convey the comment (e.g., web interface, Reddit service, mobile app, voice/text channel depending on profile).
- `Situation`: contextual situation in which the Comment event occurs.
- `CommentThread`: conversational grouping already present in Core.
- stable forums/communities/containers: map through dataset profiles and external vocabularies such as SIOC Container/Forum, ActivityStreams `context`, or Web Annotation scope where appropriate.

This avoids duplicating mature community/container vocabularies while keeping the Core domain-independent.

### Norms
Keep `Situation --governedBy--> InteractionNorm` as the preferred direction. A direct `Comment --governedBy--> InteractionNorm` can be derived/profiled if required, but should not replace the contextual relation.

## 7. Standards comparison outcome

### W3C Web Annotation
Supports an explicit Annotation/Body/Target separation and requires one or more Targets. This strongly supports adding a structural-target relation while not collapsing it into message content or semantic subject.

### ActivityStreams 2.0
Separates `inReplyTo`, `context`, `audience`, and activity `target`. This independently supports Commentium's decision to separate reply, context, audience and target-like semantics.

### SIOC
Separates `has_container`, `reply_of`, `about`, and discussion/container structures. This further supports keeping structural containment, reply and subject/topic relations distinct.

## 8. v2 candidate delta produced by P1

### New Core relation
- `anchoredTo(Comment, Commentable)`

### Renamed/refined Core relation
- `isAboutOrDirectedTo` -> `isAbout`

### Preserved distinct relations
- `respondsTo`
- `addresses`
- `refersTo`
- `involvesSubject`
- `involvesReference`

### Stereotype corrections
- `CommentSubject`: Role -> RoleMixin
- `ReferencedEntity`: Role -> RoleMixin

### Conceptual operationalization correction
- remove role reification through `playedBy` from the v2 conceptual model

### Clarifications without new classes
- narrow `Medium`
- preserve `Situation` as occurrence context
- do not add Venue/InteractionSpace yet

## 9. Decision quality / confidence

| Decision | Confidence | Remaining risk |
|---|---|---|
| Add `anchoredTo` | High | exact cardinality may be profile-specific |
| Separate anchor/reply/aboutness/reference/audience | Very high | naming can still be refined |
| `CommentSubject` -> RoleMixin | Very high | OWL transformation choice must be documented |
| `ReferencedEntity` -> RoleMixin | Very high | same |
| Remove role reification from conceptual v2 | High | migration affects current OWL examples and mappings |
| No new Venue/InteractionSpace class | Medium-high | hold-out datasets may later show a core-level invariant not captured by mappings |
| Keep Commentable as Mixin for now | Medium | full OntoUML meta-property analysis may motivate RoleMixin/refactoring later |

## Next gate
Proceed to build the first Commentium v2 candidate conceptual relation/class table and then stress-test these P1 decisions against the design datasets before modifying the canonical OWL.