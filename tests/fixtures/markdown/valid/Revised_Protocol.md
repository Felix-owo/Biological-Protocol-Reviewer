# Revised_Protocol.md

## 1. 文档控制

| Field | Value |
| --- | --- |
| SOP title | Demo flow cytometry staining SOP |
| Version | test-fixture |
| Owner | Core facility |

## 2. SOP快速执行摘要

Process each independently prepared sample through staining, washing, acquisition, and QC release before analysis.

## 3. 开始前准备

- Confirm instrument configuration and antibody panel.
- Prepare positive-control and negative-control samples.
- Label all tubes with sample ID, operator, and processing batch.

## 4. 实验步骤

1. Transfer the prepared sample to the labeled staining tube.
2. Add the defined antibody mix and record lot identifiers.
3. Incubate for the validated staining interval specified in the local panel sheet.
4. Wash, resuspend, and acquire events using the approved cytometer settings.

## 5. 试剂配制

| Reagent | Preparation | Record |
| --- | --- | --- |
| Antibody mix | Prepare from documented clones and lots in the panel sheet. | clone, catalog, lot |
| Viability dye | Prepare from current lot worksheet. | lot, dilution, operator |

## 6. 试剂、耗材、仪器

| Item | Identifier | Purpose |
| --- | --- | --- |
| Flow cytometer | instrument ID recorded before acquisition | acquisition |
| Antibody panel | panel version recorded before staining | staining |

## 7. 质量控制

| Gate | Acceptance threshold | Fail action |
| --- | --- | --- |
| Viable-cell percentage | local threshold defined in approved panel sheet | repeat preparation or exclude with deviation record |
| FMO threshold | FMO separates negative and positive population | revise gate before release |

## 8. 时间安排

Total bench time is recorded per batch with staining, washing, and acquisition timestamps.

## 9. 暂停点

Pause only after documented fixation or at a validated storage point listed in the panel sheet.

## 10. 疑难排查

| Problem | Action |
| --- | --- |
| Low viable-cell percentage | Repeat sample preparation and document exclusion reason. |
| Weak positive-control signal | Check antibody lot, compensation, and acquisition settings. |

## 11. 预期结果

Positive-control samples show the expected target population, and negative-control samples remain below the FMO-defined gate.

## 12. 数据分析

Export raw FCS files, gating workspace, compensation matrix, panel version, and QC release table.

## 附录A 设计依据

Brief rationale for control placement and release gates.

## 附录B 安全与治理

Institutional biosafety and sample-handling approvals are recorded before execution.

## 附录C 批次记录

Record sample ID, operator, date, instrument ID, panel version, and acquisition file name.

## 附录D 资源身份

Record antibody clone, catalog number, RRID when available, lot, and vendor.

## 附录E 仪器设置

Record cytometer configuration, laser/filter set, compensation matrix, and acquisition template.

## 附录F QC release

Store viability percentage, FMO threshold, event count, and release decision.

## 附录G 偏差记录

Document deviation, affected samples, root cause, rescue action, and final decision.

## 附录H Raw-data manifest

List FCS files, gating workspace, checksum, software version, and storage location.

## 附录I Prepared reagent batches

Record preparation date, operator, lot, and expiry for every prepared reagent.

## 附录J Source table

Record source identity, PMID/DOI/official URL, access date, and linked SOP section.

## 附录K Assumptions and parameter provenance

Record assumptions, who must confirm them, parameter value, source, and local verification status.
