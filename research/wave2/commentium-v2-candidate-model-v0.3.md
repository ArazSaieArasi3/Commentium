# Commentium v2 Candidate Conceptual Model v0.3

Status: candidate for Gate C validation. This revision preserves the 22-concept inventory and corrects the formal orientation of event-participation relations before official OntoUML verification.

## Delta from v0.2

### 1. Participation orientation

OntoUML `participation` connects an **endurant** to an **event in which it participates**. The conceptual OntoUML model therefore uses the formal directions below:

- `Commentable --anchors--> Comment`
- `Medium --mediumParticipatesIn--> Comment`
- `Commenter --authors--> Comment`
- `Agent --performsInterpretation--> Interpretation`
- `CommentMessage --messageParticipatesInInterpretation--> Interpretation`
- `InterpretiveAssumption --assumptionUsedIn--> Interpretation`

The future OWL/API vocabulary may expose domain-friendly inverse properties such as `anchoredTo`, `via`, `hasCommenter`, `performedBy`, `interpretsMessage`, and `basedOn`. The inverse surface direction must not be confused with the OntoUML stereotype orientation.

### 2. Structural anchor clarification

`Commentable` remains a `historicalRoleMixin` borne by persistent endurants/resources. A prior `Comment` event is **not** used as a `Commentable` merely because a platform schema calls its record a parent comment.

For a nested conversation:
- `respondsTo` points to the prior `Comment` event;
- structural anchoring points to the persistent resource/information object that hosts the new comment (e.g., a parent message/post/page according to the mapping profile).

This strengthens the Comment-event versus CommentMessage/resource distinction and prevents an event from being forced into a functional-complex RoleMixin.

### 3. Time correction

`Time` changes from `quality` to **datatype** in v0.3. Commentium operational evidence records temporal values/intervals (timestamps and related temporal qualifications). Treating Time as an intrinsic Quality of a Comment event was not sufficiently justified. Profiles may align `Time` with standard temporal datatypes or richer temporal ontologies without introducing a new Core class.

### 4. More explicit specialized event relations

Where an OntoUML event stereotype has a clear ontological justification:
- `Comment --hasMessage--> CommentMessage` is encoded as `creation`;
- `Comment --reflects--> Stance` is encoded as `manifestation`;
- `Interpretation --producesMeaning--> InterpretedMeaning` is encoded as `creation`;
- `Comment --partOfThread--> CommentThread` remains `participational` event decomposition.

Relations without a sufficiently strong UFO-specific commitment remain generic instead of receiving an artificial stereotype.

## Core inventory v0.3

The concept count remains **22**:

| Concept | v0.3 stereotype |
|---|---|
| Comment | event |
| Response | event |
| CommentThread | event |
| Commentable | historicalRoleMixin |
| Agent | category |
| Commenter | historicalRoleMixin |
| IntendedAudience | roleMixin (derived view) |
| CommentSubject | roleMixin (derived view) |
| ReferencedEntity | roleMixin (derived view) |
| Interpretation | event |
| InterpretedMeaning | kind (information-object semantics) |
| InterpretiveAssumption | kind (information-object semantics) |
| AssertedRelation | kind (propositional/information-object semantics) |
| AssertedRelationKind | enumeration |
| InteractionNorm | kind (social-object semantics) |
| Situation | situation |
| Medium | category |
| CommentMessage | kind (information-object semantics) |
| Intent | mode |
| Stance | mode |
| ExpressionStyle | quality |
| Time | datatype |

## Five target-like semantics remain invariant

1. structural anchoring (`anchors` / OWL inverse `anchoredTo`)
2. conversational predecessor (`respondsTo`)
3. semantic aboutness (`isAbout`)
4. reference in message content (`refersTo`)
5. audience/addressee (`addresses`)

They may coincide extensionally in a dataset record but are not semantically equivalent.

## Gate C policy

v0.3 may be frozen only if:
1. official OntoUML JSON Schema validation passes;
2. official `ontouml-js` parse/round-trip passes;
3. OntoUML Server verification reports zero blocking errors, or a documented incompatibility of the deployed legacy server is demonstrated while the current schema/toolchain remains green;
4. any remaining warnings are ontologically reviewed rather than silenced by artificial model elements;
5. the Amazon/Reddit/WikiConv mapping regressions remain green after these corrections.
