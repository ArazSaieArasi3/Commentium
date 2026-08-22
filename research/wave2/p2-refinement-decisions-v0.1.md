# Commentium Journal Extension — P2 Refinement Decisions v0.1

Status: preferred decisions after resolving the six P2 amber items and extending the review to whole-model OntoUML meta-properties. No canonical OWL change is made here.

## Executive decisions

| Topic | Preferred decision | Status |
|---|---|---|
| Anonymous/deleted author | Keep the ontological author existentially present; do not add `AnonymousAgent`. Missing identity is an observation/provenance issue. | ACCEPT |
| Agent stereotype | Change `Agent` from `kind` to `category` because Commentium intentionally allows heterogeneous agent identity providers (human, organization, software/institutional agents). | ACCEPT |
| Commenter stereotype | Change `Commenter` to `historicalRoleMixin`: commenter status is acquired through participation in a Comment event and may be borne by heterogeneous Agents. | ACCEPT |
| IntendedAudience | Keep as a derived `roleMixin`, broaden beyond an Agent-only implementation, and distinguish explicit audience assertions from inferred audience assertions by provenance. | ACCEPT / formal grounding to validate |
| Multimodal CommentMessage | Keep one `CommentMessage` core concept; define it as representation-neutral and potentially composite/multimodal. Do not add Image/Audio/Video classes to Core. | ACCEPT |
| Rating vs Stance | Keep raw rating outside Core as an observed/profile value. `Stance` is an analytic/intentional mode and may be inferred from rating only through an explicit interpretation/provenance step. | ACCEPT |
| Lifecycle | Keep edit/delete/restore outside Core; use PROV-O revision/invalidation/activity patterns around message/resource versions. The original Comment occurrence is not silently mutated. | ACCEPT |
| Commentable stereotype | Redefine from capability-like `mixin` to `historicalRoleMixin`: an endurant/resource is Commentable in this core sense because it has served as structural anchor in a Comment event. | ACCEPT |
| Medium stereotype | Change `Medium` from `kind` to `category`; it is a rigid non-sortal abstraction over heterogeneous channels/platforms/services. | ACCEPT |
| Response stereotype | Correct `Response` from `subkind` to `event` specializing `Comment`. `subkind` is not the proper stereotype for an event specialization. | ACCEPT |
| CommentThread stereotype | Change `CommentThread` from `collective` to a complex `event`; comments are event parts, not members of an object collective. | ACCEPT |
| Thread relation | Replace `memberOf(Comment, CommentThread)` with `partOfThread(Comment, CommentThread)` stereotyped as OntoUML `participational` event decomposition. | ACCEPT |
| Interpretation | Change from `relator` to `event` (interpretive act/process). Its current processual semantics (`interprets`, `produces`) are event-like, not a material-relation truth-maker. | ACCEPT |
| AssertedRelation | Change from `relator` to `information object` / propositional semantic artifact. An assertion in a comment must not be confused with a real-world material relation. | ACCEPT |
| AssertedRelationKind | Change from `datatype` to `enumeration`; this also restores alignment with the earlier conceptual diagram intent. | ACCEPT |
| ExpressionStyle bearer | Move expressive-style characterization from Comment event to `CommentMessage`; style characterizes informational expression, not the occurrence as such. | ACCEPT |

## P2.1 Anonymous, deleted, or unresolved authors

### Decision
No `AnonymousAgent`, `DeletedUser`, or `UnknownAuthor` Core classes are admitted.

At the conceptual level:
- every intentional Comment has at least one authoring Agent;
- the Agent's platform identifier may be unavailable, deleted, pseudonymous, or unresolved;
- lack of an identifier is epistemic/data incompleteness, not non-existence of the author.

Operational mappings may use a local opaque resource or blank node and record resolution/provenance state outside the Core.

This keeps `hasCommenter` conceptually mandatory while preventing platform-data incompleteness from weakening the ontology.

## P2.2 Agent and Commenter

A generic Commentium `Agent` can include persons, organizations/institutional agents, and software/artificial agents. These have different identity principles. Therefore `Agent` is better modeled as a rigid non-sortal `category` rather than a `kind`.

`Commenter` is not a separate role individual. It is a contextual/historical classification of the bearer. Because possible commenters can have heterogeneous identity providers, the preferred stereotype is `historicalRoleMixin`, acquired by participation in the Comment event.

## P2.3 IntendedAudience

### Decision
- keep the concept because audience is semantically distinct from subject and structural anchor;
- do not restrict it to human/user Agent identifiers;
- treat it as a derived `roleMixin` whose instances can include heterogeneous audience-bearing entities;
- `addresses` remains optional (`0..*`) because some comments do not specify an intended audience;
- explicit audience and inferred audience MUST be distinguished in provenance/operational metadata.

Inference from `respondsTo` or mentions is not automatically equivalent to explicitly intended audience.

## P2.4 Multimodal CommentMessage

`CommentMessage` remains one information-object concept and is made representation-neutral. A message can be realized through text, image, audio, video, or combinations without multiplying Core classes.

Profile/alignment layers may use Web Annotation Body resources, media types, or generic part/representation relations. This matches the Web Annotation model, which permits multiple Bodies and multiple media types while keeping them related to one Annotation.

Core rule: `Comment -> hasMessage -> CommentMessage` remains singular at the semantic-message level; representations/parts are separately multiplicative.

## P2.5 Rating versus Stance

A star/numeric rating is observed structured data. A Stance is an intentional/evaluative mode attributable to an Agent. They are not identical.

Preferred pipeline:
`raw rating -> evidence/interpretation -> Stance (optional)`

Do not assert a Stance solely because a dataset has a rating field unless a documented mapping/interpretation rule is applied.

## P2.6 Lifecycle and provenance

The Core remains synchronic/minimal. Edit, deletion, restoration, versioning, and moderator actions are handled by a provenance/lifecycle extension.

Preferred PROV-O pattern:
- message/resource revisions as `prov:Entity` versions;
- `prov:wasRevisionOf` between revisions;
- `prov:specializationOf` from version to persistent resource where useful;
- editing/moderation as `prov:Activity`;
- `prov:wasGeneratedBy`, `prov:wasAssociatedWith`, and invalidation relations for lifecycle evidence.

A Comment event is not rewritten retroactively when its message is edited; the provenance layer records subsequent activities and message/resource revisions.

## P2.7 Commentable

The old definition "entity that can receive comments" is too capability-like and semantically broad.

Preferred v2 definition:
> An entity/resource that has served as the structural anchor/host of at least one Comment occurrence.

Preferred stereotype: `historicalRoleMixin` because:
- it is anti-rigid;
- bearers may have heterogeneous identity principles;
- the classification follows participation as structural anchor in a Comment event.

`anchoredTo` provides the grounding participation relation.

This also avoids treating every potentially comment-enabled entity as a Commentable instance before any Commentium-relevant occurrence exists.

## P2.8 Response and CommentThread corrections

### Response
`Response` is a specialized type of `Comment` event. A `subkind` is a rigid specialization of an identity provider, not an event-specialization stereotype. Therefore v2 uses `Response <<event>>` specialized from `Comment <<event>>`.

### CommentThread
The v1 `CommentThread <<collective>>` + `memberOf(Comment event, CommentThread)` combination is ontologically inconsistent with OntoUML memberOf semantics, where a collective has object-like members.

Preferred v2 model:
- `CommentThread <<event>>` = a complex conversational event;
- Comment events are parts of the thread event;
- replace `memberOf` with `partOfThread` using OntoUML `participational` event decomposition.

A platform thread/container resource may still be mapped as a separate external/resource-level structural anchor; it is not identical to the conversational event.

## P2.9 Interpretation correction

The v1 `Interpretation <<relator>>` is processual in its own relations: an agent interprets a message and a meaning results. A Relator should be the truth-maker of a material relation, whereas this construct behaves as an act/process.

Preferred v2:
- `Interpretation <<event>>`;
- agent participates in the interpretation;
- the event interprets a `CommentMessage`;
- the event yields/creates `InterpretedMeaning`;
- it may be based on `InterpretiveAssumption`.

This eliminates a relator-with-process-semantics mismatch.

## P2.10 AssertedRelation correction

An `AssertedRelation` represents relational content asserted by a message; it does not guarantee that the corresponding real-world relation actually holds. Modeling it as a Relator risks conflating asserted content with a material truth-maker.

Preferred v2:
- `AssertedRelation` becomes an information/propositional object;
- it is `assertedIn` a `CommentMessage` (preferred operational domain) or traceably linked to its Comment;
- it `involvesSubject` and/or `involvesReference`;
- `AssertedRelationKind` becomes an `enumeration`.

## P2.11 Medium

`Medium` is broader than one identity-bearing Kind: a web service, channel, application, or other communication medium can instantiate it. Preferred stereotype: `category`.

Its semantics remain restricted to communication channel/platform/service and must not absorb thread/community/container identity.

## P2.12 ExpressionStyle

Preferred bearer: `CommentMessage`, not the Comment event. Expression style characterizes the informational/expression artifact.

## Remaining formal caution

`IntendedAudience`, `CommentSubject`, and `ReferencedEntity` remain derived RoleMixins in the candidate. Their relational dependence must be encoded explicitly in the formal OntoUML/OWL implementation (e.g., by derived existential definitions) and checked against FreeRole-style validation. We do **not** add three artificial relators merely to silence a validator; if the OntoUML validator requires a stronger mediation pattern, this becomes a focused Gate C decision.
