# Biological Protocol Reviewer

[中文说明](README.zh-CN.md)

[![License: MPL-2.0](https://img.shields.io/badge/License-MPL--2.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Standard-Agent_Skills-blueviolet.svg)](https://agentskills.io/specification)
[![Version](https://img.shields.io/badge/Version-v1.5.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.10--3.13-3776AB.svg)](#validation)
[![Works with](https://img.shields.io/badge/Works_with-Codex-blue.svg)](#installation)

**biological-protocol-reviewer** is a Codex skill for evidence-grounded biological protocol review with optional SOP rewriting. It audits animal, cell, molecular, flow/imaging, omics, statistics, safety/governance, and frontier-method workflows, producing a source-backed review before any requested rewrite.


## What This Skill Produces

By default, the skill uses the `protocol_gate` profile and produces one user-facing file:

- `Review_Report.md`: protocol reconstruction, readiness score, Level 0-3 maturity gate, module activation table, benchmark evidence table, severity-ranked findings, assumption ledger, and parameter provenance. Panel synthesis, operator-burden, mini-pilot, and review-to-SOP mapping sections are included only in `protocol_full` or when explicitly marked applicable.

`Revised_Protocol.md` is produced only when the user explicitly requests an SOP
rewrite (`protocol_full`). `delta_review` limits context to changed sections and
prior open findings. See `references/runtime_profiles.md`.

The skill is intentionally not a copyeditor. It asks whether the protocol can be executed, interpreted, reproduced, audited, and governed safely.

## v1.5.0 Behavior And Contract Changes

This minor release intentionally changes the default runtime and structured contracts:

- `protocol_gate` is now the default review-only profile; SOP rewriting requires an explicit `protocol_full` request, while `delta_review` limits context to changed sections and open findings.
- Readiness uses one numeric 0-10 scale, Level 0-3 must agree with that score, and operator burden uses `low / moderate / high`.
- Claim-readout handoffs require contract version `1.0.0`, sealed root/item fields, unique source IDs, and bounded reviewer extension namespaces.
- Package checks now work in arbitrary cache directory names, release checks remain explicit, and completed YAML passports fail closed when PyYAML is unavailable.
- Behavioral benchmark gates reject keyword inventories and inconsistent readiness claims. The v1.5.0 model-output benchmark remains pending and does not claim an empirical pass rate.


## Structured Resources And Validation

This repository now mirrors the useful structure of `rigorous-science-reviewer` without copying its manuscript-review logic:

- `references/protocol_rubric.json` standardizes readiness scoring, Level 0-3 maturity gates, category weights, severity levels, and execution-readiness gates.
- `templates/issue_block_templates.json` standardizes Critical/Major/Minor/Optimization issue blocks so findings include the problem, evidence, impact, failure mode, resolution, decisive readout, and SOP location.
- `templates/source_search_hints.json` standardizes evidence-search routes for protocol parameters, dynamic standards, resource identity, controls, QC, safety/governance, and local validation.
- `schemas/*.schema.json` defines machine-checkable contracts for structured review reports, revised protocols, issue blocks, QC gates, parameter provenance, bioinformatics handoff, and optional external companion evidence.
- `scripts/lint_structured_protocol.py`, `tests/`, `.github/workflows/`, and `benchmarks/v1.0/` provide deterministic regression checks around the Markdown validator.

JSON is useful here because these resources are structured, machine-checkable, and less ambiguous than free-form prose for repeated reviewer output. The Markdown files remain the main domain guidance; the JSON files define the repeatable output contract.


## Optional Companion Ecosystem

Biological Protocol Reviewer can use external skills, official plugins, MCP
tools, or host-provided capabilities when available. These companions are
optional evidence or output aids and never replace protocol-readiness judgment,
SOP authorship, safety/governance review, QC design, or local validation.

Recommended companions:

- ChatGPT Life Science Research: public biological context, entity
  normalization, and database evidence.
- K-Dense-AI/scientific-agent-skills: literature, database, source, and standard
  lookup through skills such as `$paper-lookup`, `$database-lookup`,
  `$literature-review`, `$scientific-critical-thinking`, and
  `$scholar-evaluation`.
- GPTomics/bioSkills: downstream omics-analysis handoff, QC metadata,
  repository planning, and pipeline expectations.
- Yuan1z0825/nature-skills: publication-style protocol writing after readiness
  review is complete.
- guizang-ppt-skill / open-design / taste-skill: SOP training deck, visual
  protocol summary, or presentation output after conclusions are fixed.
- Rigorous-Reviewer: only when evaluating whether protocol-derived evidence
  supports a manuscript, proposal, or central scientific claim.

All companion outputs must be resolved to concrete source identity before they
can support SOP parameters, controls, QC gates, metadata requirements, or
reporting requirements. Unresolved companion-derived suggestions must be marked
`△TO BE CONFIRMED` or `TO BE VERIFIED BEFORE EXECUTION`.

## Evidence Standards

The skill prioritizes exact source identity and current standards. Common anchors include:

- Animal research reporting and planning: [ARRIVE 2.0](https://arriveguidelines.org/arrive-guidelines) and [PREPARE](https://norecopa.no/prepare).
- qPCR/RT-qPCR reporting: MIQE guideline, PMID [19246619](https://pubmed.ncbi.nlm.nih.gov/19246619/).
- Flow cytometry reporting: MIFlowCyt guideline, PMID [18752282](https://pubmed.ncbi.nlm.nih.gov/18752282/).
- FAIR data principles: DOI [10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18).
- Biosafety and recombinant/synthetic nucleic acid governance: [NIH Guidelines](https://osp.od.nih.gov/policies/biosafety-and-biosecurity-policy/), [CDC/NIH BMBL](https://www.cdc.gov/labs/bmbl/index.html), and [WHO Laboratory Biosafety Manual, 4th edition](https://www.who.int/publications/i/item/9789240011311).
- Resource identity: [RRID portal](https://www.rrids.org/) and journal key-resource table practices such as [Cell Press Key Resources Tables](https://www.elsevier.com/en-gb/researcher/author/tools-and-resources/key-resources-table).

Every Grade A-C benchmark source should include a DOI, PMID, official URL, manual or standard version, vendor document ID, or access date when applicable. Unsupported catalog numbers, clones, RRIDs, sequences, dosages, genotyping bands, software versions, thresholds, and sequencing depths must not be invented.

## Repository Layout

```text
.
├── biological-protocol-reviewer/        # installable Agent Skill directory
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── references/
│   │   ├── protocol_rubric.json
│   │   ├── skill_manifest.json
│   │   ├── agent_behavior_core.md
│   │   ├── runtime_profiles.md
│   │   ├── sop_traceability_and_change_discipline.md
│   │   ├── external_evidence_companion_policy.md
│   │   ├── protocol_passport.md
│   │   └── cross_skill_claim_readout_handoff.md
│   ├── templates/
│   │   ├── Review_Report_template.md
│   │   ├── Revised_Protocol_md_structure.md
│   │   ├── issue_block_templates.json
│   │   ├── protocol_passport_template.yaml
│   │   └── source_search_hints.json
│   ├── schemas/
│   │   ├── review_report.schema.json
│   │   ├── revised_protocol.schema.json
│   │   ├── issue.schema.json
│   │   ├── qc_gate.schema.json
│   │   ├── parameter_provenance.schema.json
│   │   ├── bioinformatics_handoff.schema.json
│   │   ├── external_companion_evidence.schema.json
│   │   ├── protocol_passport.schema.json
│   │   └── claim_readout_handoff.schema.json
│   ├── scripts/
│   │   ├── protocol_output_validator.py
│   │   ├── lint_structured_protocol.py
│   │   ├── check_installable_skill.py
│   │   ├── check_version_consistency.py
│   │   ├── check_protocol_passport.py
│   │   ├── check_claim_readout_handoff.py
│   │   └── run_regression_fixtures.py
│   └── examples/
│       ├── cdh5_ai14_protocol_review_example.md
│       └── regression_fixtures/
├── tests/
│   └── fixtures/
├── benchmarks/
│   └── v1.0/
├── tools/
│   └── score_protocol_benchmark.py
├── docs/
│   └── release_notes/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
│       └── validate.yml
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── pyproject.toml
├── requirements-dev.txt
└── LICENSE
```

GitHub-facing README, changelog, license, CI, tests, and benchmark definitions
live at the repository root. The installable skill is intentionally isolated in
`biological-protocol-reviewer/` so the runtime package remains clean and
self-contained while the repository remains testable.

## Installation

For a reproducible v1.5.0 release checkout:

```bash
git clone --branch v1.5.0 --depth 1 https://github.com/Felix-owo/Biological-Protocol-Reviewer.git
cd Biological-Protocol-Reviewer
```

Install from this checkout using the subpath `biological-protocol-reviewer`.
For a local install, the path that Codex resolves as the skill should point to:

```text
<repo-root>/biological-protocol-reviewer
```

Do not install the repository root as the skill directory, because the root
also contains GitHub documentation.

## Core Workflow

1. Reconstruct the intended result, primary readout, experimental unit, decisive QC gates, most fragile step, and conclusion supported by the protocol.
2. Route the protocol through internal modules: animal, cell, molecular biology, flow/imaging, omics, statistics, safety/governance, frontier methods, materials/equipment, data records, operator burden, and mini-pilot validation.
3. Build an evidence dossier separating original-protocol facts, external benchmarks, recommendations, local assumptions, unresolved gaps, and optional companion-derived source leads.
4. Use external companions only as evidence-discovery, source-identity, downstream-analysis handoff, or output-conversion aids; do not delegate SOP judgment.
5. Benchmark parameters and controls against peer-reviewed protocols, top-journal methods, official standards, vendor/instrument manuals, core-facility SOPs, and local validation.
6. Run safety/governance red lines.
7. Audit failure modes and assign severity using `references/protocol_rubric.json` and `templates/issue_block_templates.json`.
8. Produce the review report; rewrite the protocol as SOP-first Markdown only when explicitly requested.
9. Validate the report and, when present, the SOP with the applicable linter and executable validator.

## Validation

For the default review-only deliverable, run:

```bash
python3 biological-protocol-reviewer/scripts/protocol_output_validator.py --profile protocol_gate --report Review_Report.md
```

When an SOP rewrite was explicitly requested, use `--profile protocol_full` and
add `--protocol Revised_Protocol.md`. For a revision delta, use
`--profile delta_review`; the report must list the prior review, changed artifact,
prior-open, resolved, new, and carried-forward IDs. The validator checks the files supplied,
including report structure, optional protocol section order, unresolved vague
language, and missing provenance. Strict content checks are enabled by default.
`--lenient-content` is only for identified legacy, non-decision drafts and must
not be used for an execution-readiness gate; JSON output marks it as
`decision_eligible: false`. The validator does not replace
scientific judgment.

For structured JSON audit extracts, Protocol Passport artifacts, or regression fixtures, run:

```bash
python3 biological-protocol-reviewer/scripts/lint_structured_protocol.py tests/fixtures/structured/valid_review_report.json
python3 biological-protocol-reviewer/scripts/lint_structured_protocol.py Revised_Protocol.structured.json --schema biological-protocol-reviewer/schemas/revised_protocol.schema.json
python3 biological-protocol-reviewer/scripts/check_protocol_passport.py tests/fixtures/structured/passport_valid_minimal.json
python3 biological-protocol-reviewer/scripts/check_claim_readout_handoff.py biological-protocol-reviewer/examples/regression_fixtures/handoff_figure_readout_missing_qc.json
```

For repository maintenance, run the deterministic test and benchmark-definition checks:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m ruff check .
python3 biological-protocol-reviewer/scripts/check_installable_skill.py --skill-dir biological-protocol-reviewer
python3 biological-protocol-reviewer/scripts/check_version_consistency.py --mode release --repo-root .
python3 biological-protocol-reviewer/scripts/check_protocol_passport.py biological-protocol-reviewer/templates/protocol_passport_template.yaml --allow-template
python3 biological-protocol-reviewer/scripts/run_regression_fixtures.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
python3 tools/score_protocol_benchmark.py --benchmark-root benchmarks/v1.0
```

GitHub Actions runs the same checks on push and pull request. The benchmark
definitions are versioned; CI validates their structure, while model-output
scoring should be used as a release evaluation gate rather than a routine
per-commit check.

## Safety Boundary

The skill assumes legitimate institutional work by trained personnel when the context supports compliant research. It switches to non-operational governance and safety guidance for oversight evasion, concealment of adverse events or deviations, unsafe non-laboratory execution, or harmful biological-agent creation or optimization.

## Typical Prompt

```text
Use biological-protocol-reviewer to review this protocol. Do not rewrite the SOP unless I explicitly request it.

Protocol title/version:
Purpose and primary readout:
Sample/organism/cell type/material:
Current procedure:
Reagents, consumables, kits, antibodies, primers/oligos:
Equipment, software, instrument settings:
Controls, QC, expected results:
Safety/governance context:
Downstream analysis and data output:
Preferred language/style/reference document:
```
