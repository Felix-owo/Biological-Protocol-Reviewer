# Markdown SOP style

Use this profile when creating `Revised_Protocol.md`. The goal is a clean,
directly usable Markdown SOP that can be read in Obsidian, GitHub, Codex, or a
plain text editor without document-rendering dependencies.

## Markdown layout

- Use one `#` title, `##` for major SOP sections, and `###` for operational
  stages or table subsections.
- Keep execution-facing sections before appendices: `SOP快速执行摘要`,
  `开始前准备`, `实验步骤`, `试剂配制`, resource tables, QC, timing,
  troubleshooting, anticipated results, and minimal analysis.
- Put design rationale, governance detail, audit records, source tables,
  assumption ledger, and parameter provenance in appendices.
- Keep front matter compact. The first executable step should appear before
  long rationale or governance text.
- Use stable section numbers so comments and review findings can point to exact
  SOP locations.

## Tables

- Use GitHub-flavored Markdown tables for resources, reagent setup, equipment,
  primers/oligos, antibodies/probes, QC gates, timing, troubleshooting, and
  records.
- Keep table columns narrow enough to remain readable in Markdown viewers. If a
  table becomes too wide, split it by resource type or move long notes below the
  table.
- Use explicit placeholders such as `△TO BE CONFIRMED`, `Not applicable`, or
  `TO BE COMPLETED BEFORE EXECUTION`; do not leave blank cells where the value
  is required.
- Use units in column headers when all rows share a unit. Use exact units in the
  cell when rows differ.

## Callout markers

Use inline markers rather than rendered boxes:

| Marker | Meaning |
|---|---|
| `▲CRITICAL` | Non-negotiable execution, interpretability, biosafety, or QC requirement. |
| `⚠CAUTION` | Hazard, welfare, chemical, biological, laser, sharps, or waste concern. |
| `⏱TIMING` | Hands-on or elapsed time for a step block. |
| `⏸PAUSE POINT` | Validated pause with storage condition and maximum duration. |
| `◉EXPDATE` | Expiration, shelf life, use-by, freeze-thaw, storage, or discard rule. |
| `◆QC` | Acceptance criterion, pass/fail decision, or release gate. |
| `✱TROUBLESHOOTING` | Link to troubleshooting ID. |
| `⬢RECORD` | Required record mapped to an appendix/run sheet. |
| `△TO BE CONFIRMED` | Missing item that cannot be safely inferred. |
| `★RECOMMENDED — TO BE VERIFIED LOCALLY` | Best-available recommendation requiring local verification. |

## Operator burden

- Keep only bench-critical instructions in the main SOP.
- Move audit-heavy rationale and reporting checklists to appendices.
- Every added record field must map to a failure mode, QC gate, safety/governance
  need, reproducibility need, or data-release requirement.
