# Biological Protocol Reviewer

**Biological-Protocol-Reviewer** is a Codex skill for evidence-grounded biological protocol review and SOP rewriting. It audits animal, cell, molecular, flow/imaging, omics, statistics, safety/governance, and frontier-method workflows, then turns incomplete bench notes into a source-backed review report and a directly executable SOP.

中文说明见 [README.zh-CN.md](README.zh-CN.md).

## What This Skill Produces

By default, the skill produces two user-facing files:

- `Review_Report.md`: protocol reconstruction, readiness score, Level 0-3 maturity gate, module activation table, benchmark evidence table, severity-ranked findings, assumption ledger, parameter provenance, operator-burden budget, mini-pilot plan, and review-to-SOP mapping.
- `Revised_Protocol.md`: bench-facing Markdown SOP with execution summary, before-you-begin checklist, numbered steps, reagent setup, resource/equipment/software/primer/antibody tables, QC gates, troubleshooting, anticipated results, minimal analysis, and audit-ready appendices.

The skill is intentionally not a copyeditor. It asks whether the protocol can be executed, interpreted, reproduced, audited, and governed safely.

## Why JSON Format Resources Were Added

This repository now mirrors the useful structure of `rigorous-science-reviewer` without copying its manuscript-review logic:

- `references/protocol_rubric.json` standardizes readiness scoring, Level 0-3 maturity gates, category weights, severity levels, and execution-readiness gates.
- `templates/issue_block_templates.json` standardizes Critical/Major/Minor/Optimization issue blocks so findings include the problem, evidence, impact, failure mode, resolution, decisive readout, and SOP location.
- `templates/source_search_hints.json` standardizes evidence-search routes for protocol parameters, dynamic standards, resource identity, controls, QC, safety/governance, and local validation.

JSON is useful here because these resources are structured, machine-checkable, and less ambiguous than free-form prose for repeated reviewer output. The Markdown files remain the main domain guidance; the JSON files define the repeatable output contract.

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
├── Biological-Protocol-Reviewer/        # installable Codex skill directory
│   ├── SKILL.md
│   ├── skill_manifest.json
│   ├── references/
│   │   ├── protocol_rubric.json
│   │   ├── module_activation_and_routing.md
│   │   ├── evidence_benchmarking_workflow.md
│   │   ├── evidence_and_standards_hard_gates.md
│   │   ├── risk_classification_and_redlines.md
│   │   └── output_qc_linter.md
│   ├── templates/
│   │   ├── Review_Report_template.md
│   │   ├── Revised_Protocol_md_structure.md
│   │   ├── issue_block_templates.json
│   │   └── source_search_hints.json
│   ├── validators/
│   │   └── revised_protocol_qc_checklist.md
│   ├── scripts/
│   │   └── protocol_output_validator.py
│   └── examples/
│       └── cdh5_ai14_protocol_review_example.md
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
└── LICENSE
```

GitHub-facing README, changelog, and license files live at the repository root.
The installable skill is intentionally isolated in
`Biological-Protocol-Reviewer/` so the Codex skill package remains clean and
self-contained.

## Installation

Install from this repository using the subpath `Biological-Protocol-Reviewer`.
For a local install, the path that Codex resolves as the skill should point to:

```text
<repo-root>/Biological-Protocol-Reviewer
```

Do not install the repository root as the skill directory, because the root
also contains GitHub documentation.

## Core Workflow

1. Reconstruct the intended result, primary readout, experimental unit, decisive QC gates, most fragile step, and conclusion supported by the protocol.
2. Route the protocol through internal modules: animal, cell, molecular biology, flow/imaging, omics, statistics, safety/governance, frontier methods, materials/equipment, data records, operator burden, and mini-pilot validation.
3. Build an evidence dossier separating original-protocol facts, external benchmarks, recommendations, local assumptions, and unresolved gaps.
4. Benchmark parameters and controls against peer-reviewed protocols, top-journal methods, official standards, vendor/instrument manuals, core-facility SOPs, and local validation.
5. Run safety/governance red lines.
6. Audit failure modes and assign severity using `references/protocol_rubric.json` and `templates/issue_block_templates.json`.
7. Rewrite the protocol as a SOP-first Markdown document, keeping bench-critical steps in the main body and audit rationale in appendices.
8. Validate the outputs with the linter, checklist, and executable validator.

## Validation

When deliverable files exist, run:

```bash
python3 Biological-Protocol-Reviewer/scripts/protocol_output_validator.py --report Review_Report.md --protocol Revised_Protocol.md
```

The validator checks required report and protocol sections, section order, unresolved vague language, and missing provenance for recommended parameters. It does not replace scientific judgment.

## Safety Boundary

The skill assumes legitimate institutional work by trained personnel when the context supports compliant research. It switches to non-operational governance and safety guidance for oversight evasion, concealment of adverse events or deviations, unsafe non-laboratory execution, or harmful biological-agent creation or optimization.

## Typical Prompt

```text
Use Biological-Protocol-Reviewer to review and rewrite this protocol.

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
