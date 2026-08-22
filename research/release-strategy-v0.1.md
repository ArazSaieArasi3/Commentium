# Commentium v2 Release Strategy v0.1

Status: proposed release policy for the journal-development line.

## Principle

Do not equate a research branch, candidate model, or green design-dataset stress test with a stable ontology release. Commentium v2 should be released only when the conceptual model, machine-readable ontology, executable tests, evaluation evidence, documentation, and manuscript are synchronized.

## Version plan

### Current baseline
- `v1.0` / v1.x: published-conference baseline and current public ontology baseline.
- Treat this line as immutable except for clearly documented metadata/packaging corrections.

### Internal candidate phase — now
- Working branch: `journal-v2-discovery`.
- Candidate artifacts may use document-level versions such as `v0.1`, `v0.2`.
- **No GitHub stable release yet.**

### First public pre-release — `v2.0.0-rc.1`
Create only after all of the following are true:
1. P1 and P2 conceptual decisions are complete.
2. Commentium v2 conceptual model is frozen at Gate C.
3. Full OntoUML anti-pattern/meta-property/cardinality review passes.
4. Canonical OWL 2 implementation is synchronized with the conceptual model.
5. SHACL constraint layer exists for non-OWL constraints where appropriate.
6. Core competency questions have executable SPARQL tests.
7. HermiT/ROBOT/syntax/SHACL checks are green.
8. Design-dataset mappings for Amazon, Reddit and WikiConv pass reproducibly.
9. Repository structure, changelog, migration notes and automated CI are present.
10. No known P1 semantic defect remains open.

Purpose of `rc.1`: expose a stable candidate for independent hold-out evaluation without claiming final generalizability.

### Stable journal artifact — `v2.0.0`
Create only after:
1. `v2.0.0-rc.1` has been frozen.
2. Hold-out evaluation is completed on datasets not used for ontology design (planned: Stack Exchange + Civil Comments, subject to final availability/legal checks).
3. Generalizability metrics and gap logs are complete.
4. Expert validation is complete or explicitly justified if omitted.
5. External alignment suite is complete for the selected standards.
6. Reproducibility/CI is green from a clean checkout.
7. Manuscript tables, diagrams, counts, constraints and ontology artifacts are synchronized.
8. Conference-to-journal delta is audited.
9. Final simulated reviewer / pre-submission quality gate passes.

**Release `v2.0.0` immediately before journal submission so the manuscript cites an immutable research artifact.**

## Post-submission policy

- Reviewer-driven non-breaking fixes: `v2.0.1`, `v2.0.2`, etc.
- New backward-compatible capability/extension material: `v2.1.0`.
- Breaking conceptual redesign: next major version.

## Recommended archival practice

At the stable release gate, archive the release in a research repository such as Zenodo if practical and cite the immutable DOI/version from the manuscript. Do not cite the moving `main` branch as the sole research artifact.

## Baseline hygiene before v2

Before the first v2 pre-release, verify whether the historical v1.0 baseline has an actual immutable Git tag/GitHub Release. If not, create a clearly documented baseline tag/release from the correct historical commit rather than pretending the current moving branch is the original release.

## Gate mapping

- Now: Wave 2 candidate / no release.
- Gate C: conceptual freeze + implementation/test completion -> eligible for `v2.0.0-rc.1`.
- Gate D: hold-out evaluation freeze -> candidate for stable packaging.
- Gate E: manuscript/repository synchronization freeze -> publish `v2.0.0`, then submit the journal manuscript.