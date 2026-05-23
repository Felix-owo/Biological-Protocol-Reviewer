# Changelog

## v1.4.0 - 2026-05-23

- Added `references/agent_behavior_core.md` for task-boundary reconstruction, anti-slop discipline, no-faux-precision, assumption-ledger, and verification-contract behavior.
- Added `references/sop_traceability_and_change_discipline.md` to require each SOP edit to map to a review issue, failure mode, readout contract, parameter-authority class, safety/governance requirement, or user-supplied fact.
- Updated `SKILL.md` routing to load the new behavior and SOP-change traceability references without replacing the v1.3.3 module architecture.
- Updated `skill_manifest.json` and the installable-skill checker to treat the new files as package integrity requirements.
- Switched repository licensing metadata from inconsistent all-rights-reserved/MIT markers to MPL-2.0 across `LICENSE`, `SKILL.md`, `pyproject.toml`, and README badges.

## v1.3.3 - 2026-05-22

- Renamed the installable skill package to canonical Agent Skills style:
  `biological-protocol-reviewer`.
- Added `agents/openai.yaml`, installability smoke checks, version consistency
  checks, and bundled regression-fixture validation.
- Moved runtime package metadata and QC checklist resources into `references/`
  so the skill package keeps standard top-level resource directories.
- Added GitHub engineering root files: `CONTRIBUTING.md`, `SECURITY.md`,
  `pyproject.toml`, `requirements-dev.txt`, Dependabot config, pull request
  template, and issue templates.
- Expanded CI to Python 3.10, 3.11, and 3.12 with JSON validation, script
  compilation, installable package checks, regression fixtures, unit tests, and
  benchmark-definition validation.

## v1.3.0 - 2026-05-21

- Added `references/external_evidence_companion_policy.md` to support optional external skills, official plugins, MCP tools, and output companions without delegating SOP judgment.
- Added companion-derived source identity gates to evidence benchmarking and standards hard-gate guidance.
- Added optional `External Evidence Companion Results` table to the review report template.
- Added `external_companion_evidence.schema.json` and optional structured report support for companion evidence provenance.
- Updated README files to mirror the Rigorous-Reviewer v2.1.0 companion-ecosystem style while preserving Biological-Protocol-Reviewer single-skill boundaries.

## v1.2.0 - 2026-05-21

- Added schema-based structured-output contracts for review reports, revised protocols, issue blocks, QC gates, parameter provenance, and bioinformatics handoff.
- Added a dependency-free structured JSON linter for CI and regression fixtures.
- Added unit tests, valid/invalid fixtures, golden-output expectations, and a versioned benchmark set.
- Added GitHub Actions CI for deterministic validation on push and pull request.
- Kept default user-facing deliverables as `Review_Report.md` and `Revised_Protocol.md`.

## v1.1.3 - 2026-05-20

- Removed an unreferenced legacy SOP rewrite reference now superseded by the Markdown SOP template and output linter.
- Added explicit navigation to the assumption ledger and parameter provenance reference.
- Replaced machine-specific absolute validation paths in validation documentation with a repository-local ignored cache path.
- Strengthened frontier-method safety limits for regulated biological delivery systems.

## v1.1.2 - 2026-05-20

- Changed the default revised protocol output from `Revised_Protocol.docx` to `Revised_Protocol.md`.
- Removed DOCX rendering and office-suite visual QA from the default workflow.
- Updated the validator to check Markdown SOP files with `--protocol Revised_Protocol.md`.
- Replaced the DOCX style profile with a Markdown SOP structure profile.
- Kept SOP content requirements intact: bench-facing steps, reagent setup, resource tables, QC gates, troubleshooting, anticipated results, data analysis, and audit-ready appendices.

## v1.1.1 - 2026-05-20

- Isolated the installable Codex skill into `Biological-Protocol-Reviewer/`.
- Kept repository-level README, changelog, and license files at the GitHub root.
- Updated validation examples to run through the isolated skill subdirectory.
- Updated DOCX style guidance to use canonical `Smiley Sans` / `得意黑` heading font without extra bold styling.
- Synchronized `SKILL.md` and `skill_manifest.json` to version `1.1.1`.

## v1.1.0

- Added structured rubric, issue-block templates, and source-search hints.
- Added executable protocol output validator.
- Strengthened evidence, operator-burden, mini-pilot, resource-identity, FAIR-data, and safety-governance gates.

## v1.0.0

- Initial public skill release.
