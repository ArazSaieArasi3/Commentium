# Commentium Journal Extension — Wave 2 Dataset Manifest v0.1

Status: discovery baseline; no raw third-party dataset content is stored in this repository.

## Allocation

| Dataset | Family | Role | Primary structures used | Raw data policy |
|---|---|---|---|---|
| Amazon Reviews 2023 | E-commerce reviews | Design | reviewer, review text/title, rating, item/parent item, timestamp, helpful votes, verified purchase, image attachments | Reference/sample locally only; do not redistribute raw corpus |
| ConvoKit Reddit Corpus | Social conversation | Design | speaker, utterance, conversation, reply-to, timestamp, score, top-level comment, subreddit/venue metadata | Use bounded reproducible sample where permitted |
| WikiConv | Collaborative discussion | Design | speaker, conversation, reply-to, comment action type, modification/deletion/restoration provenance, toxicity metadata | Use bounded reproducible sample where permitted |
| Stack Exchange public data | Q&A/community | Hold-out | posts, comments, users, parent/host post, scores, history, votes | Keep untouched until core freeze except acquisition/schema verification |
| Civil Comments | Publisher/news comments | Hold-out | comment text, parent comment, article/publication context, timestamp, moderation/toxicity labels | Keep untouched until core freeze except acquisition/schema verification |
| GoEmotions | Emotion-annotated comments | Extension probe | emotion labels over Reddit comments | Never use to justify Core concepts unless independent foundational evidence exists |
| ChangeMyView / related ConvoKit corpora | Argumentation/persuasion | Extension probe | conversational stance/persuasion/disagreement patterns | Extension-boundary probe only |

## Sampling principles

1. Design sampling must maximize structural diversity, not merely record count.
2. Sampling strata should include roots, direct replies, deep replies, referenced targets, explicit/implicit audiences, positive/negative evaluations, high/low feedback, and lifecycle/moderation cases where available.
3. Hold-out datasets must not contribute candidate Core concepts before the Core freeze.
4. If a hold-out observation cannot be represented after freeze, it is logged as post-freeze evidence; the Core is not silently modified.
5. Raw copyrighted or redistribution-restricted corpora are not committed to the repository. The repository stores manifests, schemas, identifiers, transformations, derived mappings, and permitted synthetic/minimal examples.

## Schema observations relevant to Commentium

### Amazon Reviews 2023
- Review author identity (`user_id`)
- Review message (`title`, `text`, optional images)
- Evaluated item (`asin`, `parent_asin`)
- Rating
- Timestamp
- Helpful-vote count
- Verified-purchase flag

### ConvoKit Reddit
- Speaker
- Utterance text
- Conversation identifier
- Explicit `reply_to`
- Timestamp
- Score / social feedback
- Top-level-comment relation
- Subreddit / venue metadata

### WikiConv
- Speaker
- Conversational utterance
- Conversation and reply relations
- Timestamp
- Action type
- Modification/deletion/restoration ancestry
- Revision identifiers
- Optional toxicity/moderation metadata

### Hold-out stress dimensions
Stack Exchange stresses comment-on-post versus reply semantics, post/comment separation, user deletion, voting, accepted answers and content lifecycle. Civil Comments stresses parent context, article/publication context and moderation labels without stable user identifiers.

## Next executable step
Build the evidence registry by mapping each observed phenomenon to: current Commentium coverage, candidate refinement, reuse/alignment target, UFO/OntoUML question, and provisional Core/Extension/Reject status.