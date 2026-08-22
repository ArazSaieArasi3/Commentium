# Commentium v2 Design-Dataset Mapping Profiles

Status: executable mapping harness v0.1.

This directory contains reproducible field-level mapping profiles for the three design families used before Gate C: Amazon Reviews 2023, ConvoKit Reddit, and WikiConv.

## Evidence boundary

The repository does **not** redistribute third-party corpus content. The committed JSONL files under `examples/` are synthetic schema fixtures created only to exercise mapping logic. Public source-schema documentation is recorded in each profile. Running the same adapters on bounded real samples is a separate evidence step and is required before claiming external dataset portability.

## Mapping policy

- Core mappings are asserted only when directly supported by source structure.
- Platform-specific fields such as rating, score, toxicity, revision id, verified purchase, and lifecycle action type remain in the mapping/profile namespace.
- Reddit/WikiConv `reply_to` becomes `cm:respondsTo` only when it targets a mapped prior Comment event; a reply to a structural root/post/header is not silently reinterpreted as a Comment-to-Comment reply.
- Structural anchors remain `cm:Commentable` resources and are distinct from reply-event targets.
- Amazon product identity can be both structural anchor and semantic subject because the review relation supplies direct aboutness evidence; the two predicates remain distinct.
- No inferred audience, stance, toxicity class, or lifecycle class is added to the Core.

## Public schema sources

- Amazon Reviews 2023: McAuley Lab dataset card / public README.
- ConvoKit Reddit: ConvoKit Reddit corpus and generic data-format documentation.
- WikiConv: Cornell WikiConv ConvoKit documentation.

Exact URLs and field evidence are stored in the JSON mapping profiles.

## Execution

```bash
python scripts/map_design_datasets.py
python scripts/test_mapping_portability.py
```

Generated RDF and validation reports are written under `validation-results/mappings/` and uploaded as CI artifacts.
