# Commentium Ontology

*An ontology for modeling, integrating, and interpreting comments as context-embedded communicative events.*

## Overview

Commentium is an ontology for modeling, integrating, and interpreting comments across heterogeneous social platforms and digital environments. It conceptualizes comments not as isolated text fragments or lightweight metadata nodes, but as context-embedded communicative events situated within participation structures, interpretive processes, interaction settings, and expressive conditions.

The ontology is intended to support semantic integration of comment data originating from multiple sources, including social networks, review systems, discussion platforms, and other comment-enabled environments. Its long-term objective is to provide a reusable semantic foundation for interoperable, interpretable, and explainable comment analysis across platforms, datasets, and analytical workflows.

Commentium is designed to evolve over time. While the current release provides an initial public OWL operationalization of the model, the broader trajectory of the ontology includes progressive enrichment of its formal axioms, domain extensions, and semantic capabilities.

## Vision and Evolution

Commentium is conceived as an evolving ontology rather than a static artifact. Its development trajectory is guided by the idea that comment analysis should move beyond text-centric processing toward semantically grounded and structurally transparent representations of communicative activity.

The long-term vision of Commentium is to support a family of progressively richer capabilities for comment-centered systems, including semantic interoperability across platforms, traceable interpretation of comment meaning, explainable analytical pipelines, and extensible integration with complementary ontological layers such as affective, argumentative, and domain-specific modules.

The present release represents version 1.0 of this trajectory. It delivers the baseline ontological structure, its initial OWL operationalization, and the core conceptual commitments required for future extensions.

## Scope of the Ontology

Commentium focuses on the ontological representation of comments as communicative events. It models not only the existence of a comment and its message content, but also the roles of participants, interpretive mediation, target entities, contextual situations, interaction norms, and expressive characteristics.

The ontology is intended for semantic modeling and integration rather than for direct storage optimization or platform-specific schema replacement. It is not a complete application schema for any single social platform, and it is not restricted to a single data source or review environment. Instead, it provides a domain-level ontology that can be aligned with heterogeneous comment data while preserving key ontological distinctions.

Version 1.0 should therefore be understood as a foundational operational release of the ontology rather than as the final or exhaustive endpoint of its development.

## Ontological Foundations

Commentium is grounded in the Unified Foundational Ontology (UFO) and originally specified in OntoUML. Its design relies on explicit ontological distinctions among events, kinds, roles, relators, modes, qualities, collectives, and situations.

This grounding is important because the ontology is intended to avoid common conceptual conflations in comment modeling, especially the reduction of comments to text alone or the treatment of user-generated comments as mere metadata records. In Commentium, a comment is modeled as a communicative event. Its message is treated as an informational artifact, its interpretation is treated as a mediated semantic construct, and its contextual embedding is treated as ontologically significant rather than incidental.

The OWL file provided in this repository constitutes an initial machine-readable operationalization of that ontologically grounded conceptual model.

## Repository Contents

| File / Resource | Description |
|---|---|
| `commentium.owl` | Main OWL serialization of the Commentium ontology |
| `README.md` | Human-readable documentation of the ontology |
| `LICENSE` | Repository reuse policy |
| ontology diagram image | Visual conceptual representation of the ontology |

Additional documentation and derived artifacts may be added in future versions.

## Ontology Design Summary

Commentium is organized around the idea that comments are communicative events embedded in a broader semantic and social structure. The ontology distinguishes between the event of commenting and the informational content that the comment conveys. It also separates stable identity-bearing agents from the contextual roles they play, and it treats interpretation as a distinct ontological layer rather than as an implicit property of text.

The model can be understood as consisting of five interconnected subdomains:

- **Conversation**: comment events, responses, threads, targets, medium, and time
- **Interpretation**: message content, interpreted meaning, interpretive assumptions, and asserted relations
- **Identity**: agents and their scoped participatory roles
- **Expression**: intent, stance, and expression style
- **Governance**: situation and interaction norms

This structure supports semantic clarity while remaining extensible across platforms and analytical contexts.

## Core Concepts

| Concept | Stereotype | Description |
|---|---|---|
| Comment | event | A communicative event representing the act of commenting within a structured interaction context. |
| Response | subkind | A specialized Comment that stands in a reply relation to another Comment. |
| CommentThread | collective | A collective structure aggregating related comments into a coherent thread. |
| Commentable | mixin | Any entity that can receive or host comments. |
| Agent | kind | An identity-bearing entity capable of participating in comment-related interactions. |
| Commenter | role | A scoped role played by an Agent that authors a Comment. |
| IntendedAudience | role | A scoped role played by an Agent addressed by or targeted by a Comment. |
| CommentSubject | role | The entity about which a Comment is directed or evaluated. |
| ReferencedEntity | role | An entity explicitly or implicitly referred to in comment content. |
| Interpretation | relator | A mediating semantic construct that connects an Agent, a CommentMessage, and the resulting meaning. |
| InterpretedMeaning | information object | The meaning produced through interpretation rather than directly stored in the text itself. |
| InterpretiveAssumption | information object | A contextual or semantic assumption supporting interpretive construction. |
| AssertedRelation | relator | A relational construct representing an asserted semantic relation expressed in a comment. |
| AssertedRelationKind | datatype | A controlled vocabulary used to type asserted relations. |
| InteractionNorm | social object | A normative element governing the interaction context in which a comment occurs. |
| Situation | situation | The contextual setting in which a comment event takes place. |
| Medium | kind | The communicative medium or platform through which a comment is expressed. |
| CommentMessage | information object | The informational artifact associated with a Comment event. |
| Intent | mode | The motivational orientation associated with an Agent in relation to a Comment. |
| Stance | mode | The evaluative or attitudinal orientation associated with an Agent. |
| ExpressionStyle | quality | A quality characterizing the expressive manifestation of a comment. |
| Time | quality | A temporal qualification associated with the occurrence of a comment event. |

## Core Relations

| Relation | Domain | Range | Description |
|---|---|---|---|
| `hasMessage` | Comment | CommentMessage | Links a comment event to its informational message. |
| `occursIn` | Comment | Situation | Places a comment event in a contextual situation. |
| `via` | Comment | Medium | Specifies the medium or platform through which the comment occurs. |
| `hasTime` | Comment | Time | Associates the comment event with temporal qualification. |
| `hasExpressionStyle` | Comment | ExpressionStyle | Associates a comment event with its expressive quality. |
| `respondsTo` | Response | Comment | Links a response to another comment. |
| `memberOf` | Comment | CommentThread | Places a comment in a thread structure. |
| `hasCommenter` | Comment | Commenter | Connects a comment to the role of its author. |
| `addresses` | Comment | IntendedAudience | Specifies the intended audience of a comment. |
| `isAboutOrDirectedTo` | Comment | CommentSubject | Connects a comment to the entity it is about. |
| `playedBy` | role classes | Agent | Connects a role to the Agent that plays it. |
| `inheresIn` | Intent, Stance | Agent | Associates internal modes with their bearer. |
| `motivatedBy` | Comment | Intent | Links a comment to a motivating intent. |
| `reflects` | Comment | Stance | Links a comment to an evaluative stance. |
| `governedBy` | Comment | InteractionNorm | Associates a comment with the norm governing its interaction. |
| `mediatesAgent` | Interpretation | Agent | Indicates the agent involved in interpretation. |
| `interpretsMessage` | Interpretation | CommentMessage | Indicates the message being interpreted. |
| `produces` | Interpretation | InterpretedMeaning | Specifies the meaning yielded by interpretation. |
| `basedOn` | Interpretation | InterpretiveAssumption | Indicates the assumptions supporting interpretation. |
| `groundedIn` | InterpretedMeaning | InterpretiveAssumption | Grounds interpreted meaning in assumptions. |
| `assertedIn` | AssertedRelation | Comment | Indicates the comment in which a relation is asserted. |
| `involvesSubject` | AssertedRelation | CommentSubject | Indicates the subject involved in an asserted relation. |
| `involvesReference` | AssertedRelation | ReferencedEntity | Indicates the referenced entity involved in an asserted relation. |
| `refersTo` | CommentMessage | ReferencedEntity | Connects message content to referenced entities. |
| `typedAs` | AssertedRelation | AssertedRelationKind | Assigns a type to an asserted relation. |

## Constraints and Modeling Rules

| Constraint / Guideline | Description | Status in OWL |
|---|---|---|
| C1 | An asserted relation should involve at least one subject or one referenced entity. | Partially reflected |
| C2 | If a relation kind denotes citation, at least one referenced entity should be involved. | Conceptual / not fully enforced |
| C3 | If a relation denotes directed interaction, at least one subject should be involved. | Partially reflected |
| C4 | A response should not respond to itself. | Reflected |
| C5 | Response structures should remain acyclic. | Partially reflected |
| C6 | Interpreted meaning should be produced through interpretation. | Partially reflected |
| G1 | A semantically grounded comment structure should maintain explicit directionality where applicable. | Conceptual guidance |

The OWL operationalization preserves the constraints that can be directly represented or approximated in OWL 2. Some graph-level, disjunctive, or rule-like conditions remain conceptual or only partially operationalized.

## Layered Operationalization

Commentium distinguishes among three broad operational layers in order to support transparent integration and explainable analysis.

| Layer | What It Covers | Examples |
|---|---|---|
| Observed Data Layer | Elements that can be directly aligned with raw platform or dataset fields | comment records, message text, identifiers, timestamps |
| Contextual / Integration Layer | Elements derived from platform context, aggregation logic, or integration structure | medium, thread, situation, interaction norms |
| Analytical / Interpretive Layer | Elements produced through semantic enrichment, interpretation, or reasoning | stance, interpreted meaning, asserted relation typing, intent |

This layered operationalization supports interpretability by making explicit which structures are observed, which are contextual, and which are analytically derived.

## Dataset Alignment

The ontology has been aligned, at a structural level, with the Amazon Reviews dataset (2018 release), particularly with the Electronics and Books subsets used in the accompanying case study.

| Dataset Field | Ontology Target | Interpretation |
|---|---|---|
| `reviewerID` | Agent / agentId | Identity-bearing participant |
| `reviewerName` | Agent / agentName | Human-readable participant label |
| `asin` | CommentSubject / subjectIdentifier | Identifier of the evaluated target |
| `reviewText` | CommentMessage / messageText | Main comment message content |
| `summary` | CommentMessage / messageSummary | Short summary of message content |
| `overall` | Comment / ratingValue | Raw rating signal associated with the comment |
| `reviewTime` | Time / timeLiteral | Human-readable time value |
| `unixReviewTime` | Time / unixTimeValue | Machine-oriented temporal value |
| `vote` or helpfulness signal | Comment / helpfulVoteCount or helpfulVoteTotal | Interaction feedback indicator |
| `style` | CommentMessage / styleDescriptor | Contextual stylistic descriptor |

This alignment is not intended to reduce the ontology to a platform schema. Instead, it demonstrates that the ontology can support structured mapping from heterogeneous data sources while preserving ontological distinctions.

## Intended Applications

Commentium is intended to support multiple application areas related to comment representation and analysis.

| Application Area | How Commentium Helps |
|---|---|
| Cross-platform comment integration | Provides a shared semantic layer for aligning comments across heterogeneous sources |
| Review analysis | Supports structured modeling of reviews as communicative events rather than isolated text entries |
| Explainable comment analytics | Makes interpretation pathways more transparent and traceable |
| Interoperable discourse representation | Enables semantic compatibility across different data sources and platforms |
| Semantic enrichment pipelines | Supports mapping from raw fields to richer semantic constructs |
| Comment-centered knowledge graphs | Provides a reusable ontology for structuring comment-related knowledge |
| Context-aware moderation support | Supports future norm-sensitive representations of interaction contexts |
| Consumer feedback modeling | Helps represent reviews, evaluations, and referenced targets in a disciplined structure |

## Capability Roadmap

Commentium is intended to grow over time as a capability-enabling ontology for comment analysis.

| Capability | Current Support | Future Growth Direction |
|---|---|---|
| Interoperability | Strong conceptual support | Broader alignment with external vocabularies and datasets |
| Interpretability | Strong structural support | Richer interpretive trace modeling |
| Explainability | Strong conceptual support | Explicit explanation chains and reasoning support |
| Semantic traceability | Present in the current design | Finer provenance and semantic accountability layers |
| Cross-platform integration | Supported conceptually and structurally | Expanded mappings for additional platforms |
| Context-sensitive reasoning | Partially supported | Richer contextual and situational formalization |
| Norm-aware analysis | Present at conceptual level | More explicit operational modeling of norms |
| Affective extension | Not central in v1.0 | Future integration with affective ontologies |
| Argument-aware extension | Not central in v1.0 | Future alignment with argumentative discourse models |
| Formal machine-processable reasoning | Initial OWL operationalization | Richer axiomatization and validation rules |

## Current Release Status

The current public release is **Commentium v1.0**.

This release provides:
- the baseline conceptual structure of the ontology,
- its initial public OWL operationalization,
- ontology metadata and controlled vocabulary support,
- structural documentation of concepts, relations, and constraints,
- and alignment with the case-study mapping used in the associated research article.

This version should be treated as a stable baseline release rather than as the endpoint of the ontology’s development.

## How to Use

The ontology can be opened in standard OWL-aware tools such as Protégé. It can be reused as:
- a modeling reference,
- a semantic integration layer,
- a machine-readable ontology artifact,
- or a foundation for future domain and capability extensions.

Users may inspect classes, object properties, datatype properties, annotations, and controlled vocabularies directly from the OWL file.

## Documentation and Tooling

The current repository provides manual human-readable documentation through this README and a machine-readable OWL file through `commentium.owl`.

Future documentation enhancements may include:
- WIDOCO-based documentation
- pyLODE-generated documentation
- ontology quality validation pipelines
- richer release-based documentation sets

These additions are planned as part of the ontology’s future growth rather than as requirements for the present release.

## Citation

If you use Commentium in research, documentation, or system design, please cite the associated article and reference this repository version when appropriate.

Suggested citation format may be updated as the ontology evolves and publication metadata becomes finalized.

## License

This repository is released under **CC0 1.0 Universal**.

The ontology file and repository metadata are aligned with this license in order to support open reuse, extension, and integration.

## Contact / Maintainers

Maintainers and contributors currently include the authors of the associated Commentium research work.

For ontology-related questions, corrections, or extension proposals, please use the repository issue tracker or contact the maintainers through the project repository.
