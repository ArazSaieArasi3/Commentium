# Commentium v1 -> v2 Migration Guide

Status: implementation-candidate guidance after Gate C. This document may gain additional serialization examples before `v2.0.0-rc.1`, but it must not change the frozen conceptual semantics.

## Migration principle

Commentium v2 is a semantic correction and formal-strengthening release, not a schema-field expansion. Existing v1 data should be migrated by preserving intended meaning and separating relations that v1 sometimes collapsed.

## Breaking conceptual changes

| v1 construct | v2 construct / action | Migration rule |
|---|---|---|
| `Response <<subkind>>` | `Response <<event>>` specializing `Comment` | keep response instances as Comment events; preserve `respondsTo` |
| `CommentThread <<collective>>` | complex `CommentThread <<event>>` | migrate conversational grouping to event decomposition |
| `memberOf` | `partOfThread` | replace collective membership assertions with comment-event/thread-event decomposition |
| `Commentable <<mixin>>` | `Commentable <<historicalRoleMixin>>` | classify persistent structural host resources as Commentable when they anchor a Comment occurrence |
| `Agent <<kind>>` | `Agent <<category>>` | no instance rewrite normally required; broaden identity-provider semantics |
| `Commenter <<role>>` + `playedBy` | `Commenter <<historicalRoleMixin>>` borne directly by Agent | remove role-individual reification; classify the actual Agent as Commenter |
| `IntendedAudience <<role>>` | derived `RoleMixin` view | classify addressed bearer directly; preserve provenance for inferred audience |
| `CommentSubject <<role>>` Agent-only | derived `RoleMixin` view with heterogeneous bearers | classify actual product/document/person/etc. as CommentSubject; remove Agent-only assumption |
| `ReferencedEntity <<role>>` Agent-only | derived `RoleMixin` view with heterogeneous bearers | classify actual referenced entity; remove Agent-only assumption |
| `Interpretation <<relator>>` | `Interpretation <<event>>` | migrate interpretation instances as events with performer, message, and produced meaning |
| `AssertedRelation <<relator>>` | propositional/information object | treat materialized assertions as claims represented in message content, not real-world truth-makers |
| `AssertedRelationKind` datatype | enumeration individuals | migrate literal relation-kind values to controlled individuals such as `cm:cites` |
| `Medium <<kind>>` | `Medium <<category>>` | no normal instance rewrite; semantics narrowed to communication channel/platform/service |
| `Time <<quality>>` | normalized temporal datatype | migrate time objects/values to canonical `xsd:dateTime` values through `hasTime` where possible |
| `isAboutOrDirectedTo` | `isAbout` + `addresses` | split subject/aboutness from audience/addressee |
| `refersTo` drift | `CommentMessage -> ReferencedEntity` | move message-reference assertions to the message level |
| `governedBy` drift | `Situation -> InteractionNorm` | attach norms to contextual situations rather than directly to comments |
| Comment expression style | `CommentMessage -> ExpressionStyle` | move style bearer to message representation |

## Structural-target migration

v2 explicitly distinguishes five target-like meanings:

1. structural anchoring — `anchoredTo`;
2. conversational predecessor — `respondsTo`;
3. semantic aboutness — `isAbout`;
4. message reference — `refersTo`;
5. intended audience — `addresses`.

Never migrate a single v1/platform `target` or `parent` field mechanically into all five relations. The mapping profile must determine which semantics the source field actually supports.

## Participation orientation and OWL inverses

The frozen OntoUML model uses formal endurant-to-event participation directions such as:

- `Commentable anchors Comment`;
- `Commenter authors Comment`;
- `Medium mediumParticipatesIn Comment`;
- `Agent performsInterpretation Interpretation`.

The OWL/API layer exposes domain-friendly inverses:

- `Comment anchoredTo Commentable`;
- `Comment hasCommenter Commenter`;
- `Comment via Medium`;
- `Interpretation performedBy Agent`.

These inverse pairs express the same participation facts and must not be interpreted as separate domain commitments.

## Anonymous/deleted identities

Do not infer that a Comment has no author merely because a platform identifier is missing, deleted, or anonymized. Create an opaque/local Agent resource when necessary, classify it as Commenter, and record identity-resolution status/provenance in the mapping layer.

## Ratings and Stance

Do not migrate a numeric/star rating directly as an instance of `Stance`. Preserve the rating as observed source/profile data. Any Stance assertion must be produced through a documented interpretation/mapping rule.

## Lifecycle data

Edit, deletion, restoration, moderation, and verification history remain outside the Core and should be represented through provenance/lifecycle extensions aligned with PROV-O where appropriate.

## Deprecated vocabulary

The v2 OWL candidate retains the following IRIs only as deprecated vocabulary to aid migration:

- `cm:playedBy`
- `cm:memberOf`
- `cm:isAboutOrDirectedTo`

They must not be used in newly generated v2 data.

## Release migration rule

No automated in-place rewrite of the public v1 artifact is performed before the v2 implementation block passes OWL/SHACL/reasoner/CQ validation. The root `commentium.owl` remains the v1 baseline until the release-candidate gate is explicitly reached.
