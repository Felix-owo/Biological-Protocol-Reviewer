# Revised_Protocol.docx SOP-first structure

Default language: Simplified Chinese, unless the user explicitly requests another language.

This template defines the required structure for `Revised_Protocol.docx`. The document must be directly usable by trained researchers as a bench-facing SOP. Put the operational workflow in the main body, and place background, governance, design rationale, audit records, provenance, and reporting checklists in appendices unless they are needed at the bench during execution.

Use clear Word heading styles, numbered procedure steps, compact execution tables, and standardized callout symbols.

Apply the visual style tokens in `references/markdown_sop_style.md` unless the user supplies a newer reference. In brief: A4 portrait, 0.5 inch margins, LXGW WenKai/霞鹜文楷-style body font, 得意黑-style heading font, restrained table fills (`D9D6C2`, `EDEAE0`, `F7F7F2`), and sparse emphasis colors for warnings, pass/fail, and appendix references.

## 1. 标题 / Title

- Concise and specific.
- Include organism/system, experimental material, core method, and main application.

## 2. 文档控制 / Document control

Keep this compact on the first page.

| 字段 | 内容 |
|---|---|
| SOP编号 |  |
| 版本 |  |
| 生效日期 |  |
| 作者 |  |
| 审核人 |  |
| 批准人 |  |
| 适用实验室/平台 |  |
| 关联伦理/安全审批编号 | TO BE COMPLETED BEFORE EXECUTION |
| 修订历史 |  |

## 3. SOP快速执行摘要 / Bench-facing execution summary

This section replaces a long front-matter introduction. It should fit on one page when possible.

Include:

- SOP目的 and supported readout.
- Sample/input type and minimum acceptable input.
- Total hands-on time and total elapsed time.
- Required personnel/facility/instrument status.
- Critical stop/go QC gates.
- One-line safety/governance notice with appendix link.

Avoid long literature background here. Move rationale to Appendix A.

## 4. 开始前准备 / Before you begin

Use an execution checklist.

| 检查项 | 要求 | 完成/记录 |
|---|---|---|
| 样本/动物/细胞状态 |  |  |
| 试剂 thaw/prep |  |  |
| 仪器预热/校准/预约 |  |  |
| 标签、管架、板图、随机化表 |  |  |
| 原始数据目录和命名规则 |  |  |
| PPE/waste route/approval active check | See Appendix B |  |

Use `▲CRITICAL` for prerequisites that invalidate the run if missing, `⚠CAUTION` for hazards, and `⬢RECORD` for records that must be completed before starting.

## 5. 实验步骤 / Procedure

This is the main body of the SOP and must appear before long background, governance, or audit appendices.

Use numbered direct instructions grouped by stage. Each stage must include:

- Purpose of the stage in one sentence.
- Inputs and expected outputs.
- Exact sample amount, cell number, tissue mass, reaction volume, tube/plate format, or acceptable input range.
- Reagent amount/concentration, incubation time/temperature, centrifugation in ×g, wash/transfer details, and equipment settings.
- QC checkpoint and pass/fail action when relevant.
- Required record field mapped to an appendix table.
- Step-linked troubleshooting IDs.

Example structure:

### Stage 1. <stage name>

`⏱TIMING`: <duration>

1. <Direct instruction with exact parameter>. `⬢RECORD`: <record field>.
2. <Direct instruction>. `▲CRITICAL`: <non-negotiable criterion>.
3. <Direct instruction>. `◆QC`: <acceptance criterion and fail action>.

Callouts:

- `⏱TIMING` at every major stage.
- `▲CRITICAL` for essential details and interpretability requirements.
- `⚠CAUTION` for hazards.
- `⏸PAUSE POINT` for validated stops.
- `✱TROUBLESHOOTING` for steps linked to the troubleshooting table.
- `⬢RECORD` for required records.
- `△TO BE CONFIRMED` for missing information that cannot be safely inferred.
- `★RECOMMENDED — TO BE VERIFIED LOCALLY` for best-available recommended parameters.

## 6. 试剂配制 / Reagent setup

Place all prepared buffers, staining mixes, master mixes, enzyme reactions, media, collection buffers, fixation/permeabilization reagents, wash buffers, and sequencing/library-prep mixes here before the resource inventory.

For every prepared reagent:

| 配制试剂 | 用途/步骤 | 终体积/批量 | 组分 | Stock conc. | Final conc. | Volume | 配制顺序 | 混匀/过滤/避光 | 分装 | 储存 | ◉EXPDATE | 使用前QC | 弃用标准 |
|---|---|---:|---|---|---|---:|---|---|---|---|---|---|---|

Rules:

- Include per-sample volume and overage calculation where relevant.
- Specify preparation order, hold condition, filtration/sterilization, aliquot size, freeze-thaw limit, light sensitivity, and shelf life.
- Use conservative `prepare fresh`, `same day`, or `TO BE VERIFIED LOCALLY` when shelf life is not authoritative.
- Link each reagent to procedure step numbers.

## 7. 试剂、耗材、仪器、引物/oligos、抗体/探针 / Resources, equipment, primers/oligos, antibodies/probes

This section must be purchase-ready and execution-ready. Separate tables by resource type instead of one overloaded table.

### 7.1 试剂、试剂盒和耗材 / Reagents, kits, and consumables

| 类别 | 名称 | Vendor/品牌 | Cat. No./货号 | Lot记录 | Stock/working conc. | 储存条件 | ◉EXPDATE | 用途/步骤 | 来源状态 |
|---|---|---|---|---|---|---|---|---|---|

### 7.2 仪器和软件 / Equipment and software

| 设备/软件 | Vendor | Model/version | Serial/Core ID | Configuration | Calibration/maintenance | Run settings | Step used | Record field |
|---|---|---|---|---|---|---|---|---|

### 7.3 引物、oligos、barcodes、gRNAs、探针 / Primers, oligos, barcodes, gRNAs, probes

| 名称 | Type | Sequence 5'->3' | Modification/index | Target/amplicon | Working conc. | Vendor | Purification | Storage | QC/validation | Step used |
|---|---|---|---|---|---|---|---|---|---|---|

If a sequence is unknown or should come from a local validated design, write `△TO BE CONFIRMED` and state the required source.

### 7.4 抗体和染料 / Antibodies and dyes

| Target | Clone | Fluor/Conjugate | Vendor | Cat. No. | RRID | Amount/concentration per test | Titration status | Storage | ◉EXPDATE | Step used |
|---|---|---|---|---|---|---|---|---|---|---|

Missing original information must be marked `△TO BE CONFIRMED`. Recommended substitutions must be marked `★RECOMMENDED — TO BE VERIFIED LOCALLY`.

## 8. 质量控制与放行标准 / Quality control and release criteria

Keep the primary QC gates in the main body so the operator knows when to stop, rescue, repeat, or release.

| QC checkpoint | Step | Acceptance criterion | Required record | Fail action | Interpretation risk |
|---|---|---|---|---|---|

If the SOP introduces new, substituted, scaled, transferred, or locally unvalidated parameters, include a compact mini-pilot validation block here and put details in Appendix K.

| Mini-pilot item | Requirement |
|---|---|
| Purpose |  |
| Minimum design |  |
| Positive/negative controls |  |
| Acceptance threshold |  |
| Stop/go rule |  |
| Repeat/rescue/exclusion rule |  |
| Burden-control rationale |  |

## 9. 时间安排与暂停点 / Timing and pause points

### 9.1 时间安排 / Timing

| 阶段/步骤 | Hands-on time | Total elapsed time | 可并行 | 备注 |
|---|---:|---:|---|---|

### 9.2 暂停点 / Pause points

| Step | Pause condition | Storage | Maximum duration | Recovery condition | Risk |
|---|---|---|---|---|---|

## 10. 疑难排查 / Troubleshooting

| ID | Step | Problem | Most likely cause | Immediate action | Preventive QC | Repeat/rescue/exclude rule |
|---|---|---|---|---|---|---|

## 11. 预期结果 / Anticipated results

Include expected yield, purity, viability, fragment size, sequencing/library metrics, imaging/flow readout, representative good/bad outcomes, and interpretation boundaries.

## 12. 数据分析与结果解释 / Data analysis and interpretation

Include the minimal analysis workflow required to interpret the experiment:

- Software and version.
- Input files and naming convention.
- Thresholds and normalization.
- Statistical test or model.
- Exclusion rule.
- Data and figure outputs.
- Limits of interpretation.

Move long reporting checklists and full provenance to Appendix K.

## 13. 附录A：应用范围、局限性与实验设计

Include:

- Method background only as needed.
- Applications and limitations.
- Experimental unit.
- Biological and technical replicates.
- Randomization/blinding.
- Controls.
- Inclusion/exclusion criteria.
- Batch design.
- Sample-size rationale.
- Downstream readout compatibility.

Use `▲CRITICAL` for design features required for interpretability.

## 14. 附录B：治理、授权、人员资质、伦理、安全与生物安全

Use the default statement:

> This SOP assumes execution by trained and authorized personnel in an approved institutional setting. Relevant ethics, biosafety, animal-use, human-subject, chemical-safety, radiation-safety, and/or core-facility approvals are assumed to be active. Approval identifiers, personnel qualification records, and facility authorization must be recorded before execution.

Translate or supplement in Chinese.

Use `⚠CAUTION` for hazards and `⬢RECORD` for approval/personnel records.

## 15. 附录C：实验运行记录表 / Experiment run sheet

| Run ID | Date | Operator | SOP version | Experimental group | Biological replicate | Technical replicate | Start/end time | Deviations | Pass/fail |
|---|---|---|---|---|---|---|---|---|---|

## 16. 附录D：动物/细胞/样本来源记录表 / Animal/cell/sample provenance table

Retain only relevant fields and mark non-applicable fields `Not applicable`.

| Sample ID | Source | Species/strain/cell line/tissue | Genotype/sex/age/passage | Treatment group | Collection method/time | Processing start time | Storage | Freeze-thaw | Approval/source record |
|---|---|---|---|---|---|---|---|---|---|

## 17. 附录E：试剂、抗体、试剂盒、耗材批号记录表

| Item | Vendor | Cat. No. | Lot | Clone/RRID/model if applicable | Concentration | Open/prep date | Expiration | Storage | Operator |
|---|---|---|---|---|---|---|---|---|---|

## 18. 附录F：设备、软件、仪器设置记录表

| Instrument/software | Model/version | Serial/Core ID | Configuration | Calibration status | Settings file/path | Operator/facility | Run date |
|---|---|---|---|---|---|---|---|

## 19. 附录G：QC放行记录表

| QC checkpoint | Acceptance criterion | Observed value | Pass/fail | Corrective action | Disposition | Approved by |
|---|---|---|---|---|---|---|

## 20. 附录H：偏差、排除与事件记录表

| Item ID | Deviation/exclusion/incident | Root cause | Impact on interpretation | Corrective action | Disposition | Approved by |
|---|---|---|---|---|---|---|

## 21. 附录I：原始数据清单与文件索引

| File ID | File name | File type | Source instrument/software | Acquisition date | Sample IDs | Storage path | Backup status | Checksum/unique ID |
|---|---|---|---|---|---|---|---|---|

## 22. 附录J：配置试剂批次、储存与有效期记录表

| Prepared reagent | Batch ID | Preparation date | Operator | Component lots | Storage | Expiration/use-by | Freeze-thaw count | Pre-use QC | Discard record |
|---|---|---|---|---|---|---|---|---|---|

## 23. 附录K：报告清单、假设台账与参数溯源

Include reporting-standard checklists, assumption ledger, parameter provenance, source/citation table, and any long metadata tables that are important for publication or audit but not required for bench execution.

### K.1 报告清单 / Reporting checklist

| Standard/checklist | Requirement | SOP location | Status |
|---|---|---|---|

### K.2 Assumption ledger / 假设台账

| Assumption | Basis | Risk if wrong | Verification required before execution | Where used |
|---|---|---|---|---|

### K.3 Parameter provenance / 参数溯源表

| Parameter | Original value | Revised value | Provenance | Confidence | Local verification requirement |
|---|---:|---:|---|---|---|

### K.4 Source and citation table / 来源与引用表

| Source | Type/grade | Parameter or requirement supported | DOI/PMID/URL/manual version | Access date |
|---|---|---|---|---|

### K.5 Operator burden budget / 操作者负担预算

| Added requirement | Burden | Value | Keep/appendix/omit decision |
|---|---|---|---|
