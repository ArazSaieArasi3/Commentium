# Commentium v2 — Design-Dataset Mapping and Portability Harness v0.1

Date: 2026-08-22

Status: **GREEN for schema-grounded synthetic mapping fixtures; bounded real-sample execution remains open**

## Purpose

This block converts the three Gate-C design families into reproducible mapping profiles and executable RDF-generation tests without redistributing third-party corpus content.

Design families:
- Amazon Reviews 2023;
- ConvoKit Reddit;
- WikiConv.

## Source evidence

The mapping profiles are grounded in the project dataset manifest and v0.3 design-dataset regression, with field names cross-checked against the public source-schema documentation referenced in each mapping profile.

Repository evidence:
- `research/wave2/dataset-manifest-v0.1.md`
- `research/wave2/design-dataset-regression-v0.3.md`
- `research/wave2/gate-c-freeze-record.md`
- `mappings/design/*.profile.json`

## Copyright / evidence boundary

No third-party raw corpus content is committed in this harness.

The committed JSONL records under `mappings/design/examples/` are explicitly marked `synthetic: true` and exist only to exercise the documented source schemas and mapping logic. The mapping script refuses a committed regression fixture that is not explicitly synthetic.

Therefore this block establishes:
- reproducible mapping semantics;
- executable adapter behavior;
- SHACL-valid generated RDF;
- controlled cross-family query portability.

It does **not** yet establish empirical portability on bounded real records from the three third-party datasets. That is the next evidence step and is required before making an external-data portability/generalizability claim.

## Mapping artifacts

- `mappings/design/README.md`
- `mappings/design/amazon-reviews-2023.profile.json`
- `mappings/design/reddit-convokit.profile.json`
- `mappings/design/wikiconv.profile.json`
- `mappings/design/examples/*.synthetic.jsonl`
- `mappings/design/portable-queries/*.rq`
- `mappings/design/portability-manifest.json`
- `scripts/map_design_datasets.py`
- `scripts/test_mapping_portability.py`
- `.github/workflows/design-mappings.yml`

## Mapping policy

### Shared Core commitments

Every mapped Comment event receives the source-supported operational minimum:
- `cm:hasMessage`;
- `cm:anchoredTo`;
- `cm:hasCommenter`;
- `cm:occursIn`;
- `cm:via`;
- `cm:hasTime`.

### Amazon Reviews 2023

Directly represented:
- review occurrence as `cm:Comment`;
- review content as `cm:CommentMessage`;
- user as `cm:Agent` + `cm:Commenter`;
- product as structural `cm:Commentable` anchor;
- product also as `cm:CommentSubject` through `cm:isAbout`, because the review relation directly supplies evaluated-subject evidence;
- timestamp as normalized `xsd:dateTime`;
- source/service as `cm:Medium`.

Kept in profile space rather than Core:
- rating;
- verified purchase;
- helpful votes;
- representation-specific image fields.

### ConvoKit Reddit

Directly represented:
- utterance comment as `cm:Comment`;
- nested reply as `cm:Response` only when `reply_to` targets a mapped prior Comment event;
- textual content as `cm:CommentMessage`;
- speaker as `cm:Agent` + `cm:Commenter`;
- persistent post root as `cm:Commentable` structural host;
- conversation grouping as `cm:CommentThread` through `cm:partOfThread`;
- timestamp and medium.

A top-level comment whose source `reply_to` points to the Reddit post is **not** silently recast as a Response to a Comment event.

No semantic subject or intended audience is inferred solely from conversation structure.

### WikiConv

Directly represented:
- non-section-header talk-page action as `cm:Comment`;
- nested reply as `cm:Response` only when the predecessor is another mapped Comment;
- message, speaker, structural host, thread, timestamp, and medium.

Kept in profile/lifecycle space:
- action type;
- revision id;
- toxicity score;
- modification/deletion/restoration provenance.

No topic/aboutness assertion is manufactured from Talk Page structure alone.

## Generated RDF evidence

Final CI mapping generation:

| Dataset profile | Synthetic source rows | Generated RDF triples | SHACL |
|---|---:|---:|---:|
| Amazon Reviews 2023 | 1 | 23 | PASS |
| ConvoKit Reddit | 3 | 39 | PASS |
| WikiConv | 3 | 41 | PASS |

## Portable-query matrix

Five queries are executed unchanged over every generated dataset graph.

| Query | Amazon | Reddit | WikiConv |
|---|---|---|---|
| PQ01 Core context | 1 row PASS | 2 rows PASS | 2 rows PASS |
| PQ02 Reply separation | 0 rows / N/A PASS | 1 row PASS | 1 row PASS |
| PQ03 Thread participation | 0 rows / N/A PASS | 2 rows PASS | 2 rows PASS |
| PQ04 Aboutness | 1 direct row PASS | 0 / not asserted without evidence PASS | 0 / not asserted without evidence PASS |
| PQ05 Retired v1 vocabulary absent | false PASS | false PASS | false PASS |

This matrix intentionally distinguishes **not applicable**, **not asserted without evidence**, and **supported**. A capability is not fabricated merely to maximize nominal query coverage.

## CI evidence

Final mapping workflow:
- workflow: `Design Dataset Mappings`
- run id: `32573496316`
- result: **SUCCESS**
- artifact id: `9475938614`
- artifact digest: `sha256:90f6141ecbdda92450d9ffdcc923757d62e818ddd4f38bac24bca4d3c59d1f8e`

On the same mapping commit, all other semantic pipelines remained green:
- OntoUML Verify: **SUCCESS**;
- Competency Questions: **SUCCESS**;
- Semantic Artifacts / OWL 2 DL / HermiT / SHACL: **SUCCESS**.

No Gate-C conceptual change was required.

## Research interpretation

The current result is stronger than a prose-only mapping table because the mapping decisions are executable and regression-tested. However, scientific reporting must preserve the evidence boundary:

- **Current claim:** the frozen Commentium v2 Core supports reproducible schema-grounded mappings for three structurally heterogeneous design families under controlled synthetic fixtures.
- **Not yet supported:** empirical cross-dataset portability/generalizability on sampled third-party records.

## Next evidence step

Execute the same adapters on bounded real samples obtained according to each dataset's access/licensing rules. Record:
- exact source/version/access date;
- selection procedure and sample identifiers where redistribution-safe;
- input checksum or locally reproducible acquisition parameters;
- mapping success/failure counts;
- SHACL conformity;
- portable-query support;
- adaptation/mapping exceptions;
- any observation that would pressure the frozen Core.

Any genuine Core-change pressure must reopen Gate C rather than being silently absorbed by the implementation.
