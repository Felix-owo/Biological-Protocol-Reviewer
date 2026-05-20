# Changelog

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
