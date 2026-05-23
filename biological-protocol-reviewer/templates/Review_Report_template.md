# Review_Report.md template

Default language: Simplified Chinese unless the user requests otherwise.

# Protocol评审报告：<Protocol title>

## 1. Protocol身份信息

| 字段 | 内容 |
|---|---|
| 原始文件 |  |
| Protocol版本 |  |
| 实验类型 | 动物 / 细胞 / 分子 / 流式 / 成像 / 组学 / frontier / mixed |
| 目标readout |  |
| 下游用途 |  |
| 审核日期 |  |
| Skill版本 | biological-protocol-reviewer v1.4.2 |

## 2. Protocol重建 / Protocol reconstruction

| 项目 | 评审重建 | 置信度 | 缺失信息 |
|---|---|---|---|
| Intended result |  | High / Moderate / Low |  |
| Primary readout |  |  |  |
| Experimental unit |  |  |  |
| Most fragile step |  |  |  |
| Decisive QC gate |  |  |  |
| Conclusion supported by the SOP |  |  |  |

## 3. 执行摘要 / Executive verdict

| 结论项 | 判断 |
|---|---|
| 总体结论 |  |
| 当前成熟度 | Level 0 / 1 / 2 / 3 |
| 修订目标 | Level 3 publication-grade, bench-facing SOP |
| 最大失败模式 |  |
| 是否可直接执行 | 是 / 否 / 仅可在补齐指定QC后执行 |
| 最小执行前门槛 |  |

## 3.1 Protocol Readiness Contract / SOP重写前锁定条件

This section must be completed before executable SOP rewrite.

| Contract field | Locked value | Blocks execution if unresolved? | SOP handling |
|---|---|---:|---|
| Intended result |  |  |  |
| Primary readout |  |  |  |
| Experimental unit |  |  |  |
| Decisive QC gates |  |  |  |
| Local validation requirements |  |  |  |
| Red-line safety/governance checks |  |  |  |
| Parameters not to fill without authority |  |  |  |
| Level 0/1/2/3 maturity gate conditions |  |  |  |

## 4. User-supplied corpus handling / 用户材料处理

Include when the user supplied SOPs, manuals, lab notes, datasheets, primer
sheets, antibody panels, sequencing specs, analysis scripts, or local validation
records.

| Supplied item | Screened? | Used? | Exclusion reason if skipped | Protocol decision affected |
|---|---:|---:|---|---|

## 5. 模块自动判定 / Module activation table

| Module | Status | Triggering evidence from original protocol | Main risk if omitted | Reference file used |
|---|---|---|---|---|

Status must be one of: `Activated`, `Not activated — not applicable`, or `Unclear — needs confirmation`.

## 6. 金标准证据对标 / Evidence benchmark table

| Protocol component | Benchmark source identity | Grade | Exact supported parameter/requirement | Original protocol status | Reviewer decision | Version/access | Revised SOP location |
|---|---|---|---|---|---|---|---|

Grade A-C sources must include DOI, PMID, official URL, manual/standard version, vendor document ID, or access date when applicable.


## 6.1 External Evidence Companion Results (optional)

Include only when companion skills, official plugins, MCP tools, or host tools
were used. Omit when no external companion contributed evidence.

| Companion/tool | Query/entity | Returned source/identifier | Evidence role | Protocol section affected | Limitation / verification needed |
|---|---|---|---|---|---|

Companion outputs are source-discovery or context inputs. They are not Grade A-C
support unless resolved to a primary protocol, official standard, vendor or
instrument manual, core-facility SOP, repository record, or documented local
validation.

## 6.2 Parameter authority isolation / 参数权威隔离

| Parameter | Protocol location | Proposed value | Authority class | Source identity | Local validation status | SOP label |
|---|---|---|---|---|---|---|

Authority class must be one of: original protocol fact, local validated
parameter, external benchmark, vendor/manual standard, institutional/core-facility
SOP, recommended but unvalidated, unresolved gap, or companion-derived lead.

## 7. 资源完整性审计 / Resource identity audit

| 类别 | 缺vendor | 缺Cat. No. | 缺clone/RRID/model/version | 缺lot记录 | 缺储存条件 | 缺◉EXPDATE | 执行影响 | 修订处理 |
|---|---:|---:|---:|---:|---:|---:|---|---|

## 8. Severity-ranked issues

Use full issue blocks for every Critical and Major issue. Minor and Optimization issues may be shorter only when they do not affect interpretability, safety, or reproducibility.

### C<number>. <致命问题标题>

**具体问题：**  

**为什么严重：**  

**证据：** 原protocol位置；内部证据；外部标准/文献/手册证据。  

**影响：** 威胁的readout、结论、样本可用性、安全性或审计能力。  

**替代解释/漏洞：** 如果不修正，哪些伪阳性、伪阴性、批次效应、污染、偏倚或执行偏差无法排除。  

**解决：** 修订动作、需要加入的控制/QC/记录/参数。  

**决定性 readout：** 最低可接受标准、pass/fail阈值、stop/go规则。  

**SOP修订位置：**  

### M<number>. <重大问题标题>

Use the same labels: `具体问题` / `为什么重要` / `证据` / `影响` / `替代解释/漏洞` / `解决` / `决定性 readout` / `SOP修订位置`.

### m<number>. <次要问题标题>

Shorter block allowed, but still state location, problem, fix, and SOP location.

### O<number>. <优化建议标题>

Focus on robustness, efficiency, scalability, data quality, and reduced operator burden.

## 9. Readout contracts, controls, QC, and release criteria

| Readout ID | Conclusion supported | Experimental unit | Positive control | Negative/control readout | Failure mode detected | Acceptance criterion | Fail action | Interpretation boundary |
|---|---|---|---|---|---|---|---|---|

## 10. Cross-skill claim-readout handoff

Include when the protocol readout is used to support a manuscript, proposal,
figure set, dataset, or central scientific claim.

| Claim ID | Claim | Evidence role | Readout ID | Protocol step/method | Parameter authority | QC gate | Failure mode | Manuscript impact | Revision action |
|---|---|---|---|---|---|---|---|---|---|

## 11. Protocol panel synthesis

| Panel role | Finding | Severity | Readout or SOP section affected | Minimum resolution | Residual risk |
|---|---|---|---|---|---|

Required panel roles: core-facility operator, domain PI / method expert,
statistics and data reviewer, safety/governance reviewer, Devil's Advocate, SOP
synthesizer.

## 12. Controls, QC, and release criteria

| Control/QC | Failure mode detected | Original status | Required SOP location | Acceptance criterion | Fail action |
|---|---|---|---|---|---|

## 13. Metadata, records, and data-quality gaps

| Record/data item | Why it matters | Main body or appendix | Required/optional | Burden justification |
|---|---|---|---|---|

## 13.1 Data records and repository gate

Include for reusable data outputs, especially omics, flow, imaging, sequencing,
high-content screening, behavior, or computational outputs.

| Output | Raw data | Processed data | Metadata | Repository/access route | Identifier status | QC file | Retention |
|---|---|---|---|---|---|---|---|

## 14. Statistics and reproducibility

| Dimension | Current status | Risk | Required action |
|---|---|---|---|
| Experimental unit |  |  |  |
| Biological replicate |  |  |  |
| Technical replicate |  |  |  |
| Batch/blocking |  |  |  |
| Randomization/blinding |  |  |  |
| Inclusion/exclusion |  |  |  |
| Sample-size logic |  |  |  |
| Statistical test/model |  |  |  |

## 15. Safety, ethics, biosafety, and governance

Assume qualified personnel and active institutional approval when context is consistent with compliant institutional research. Missing identifiers are documentation gaps unless the request crosses a red line.

| Topic | Status | Risk | SOP placeholder/action |
|---|---|---|---|

## 16. Domain-specific review

Only include modules that were activated or marked unclear by routing.

### Animal experiments
### Cell experiments
### Molecular biology
### Flow cytometry / imaging
### Omics / computational readout
### Frontier method module
### Safety / governance

## 17. Assumption ledger / 假设台账

Include when missing context is filled, inferred, or converted into a recommended value.

| Assumption | Basis | Risk if wrong | Verification required before execution | Where used |
|---|---|---|---|---|

## 18. Parameter provenance / 参数溯源表

Include when recommended or substituted parameters are introduced.

| Parameter | Original value | Revised value | Provenance | Confidence | Local verification requirement |
|---|---:|---:|---|---|---|

## 19. Operator burden budget / 操作者负担预算

| Added requirement | Burden | Value | Keep/appendix/omit decision |
|---|---|---|---|

## 20. Local mini-pilot validation

Include when the revised SOP introduces new, substituted, scaled, transferred, or locally unvalidated parameters.

| Mini-pilot item | Requirement |
|---|---|
| Purpose |  |
| Minimum design |  |
| Positive/negative controls |  |
| Acceptance threshold |  |
| Stop/go rule |  |
| Repeat/rescue/exclusion rule |  |
| Burden-control rationale |  |

## 21. Protocol Passport summary

Include only when `Protocol_Passport.yaml` or `Protocol_Passport.json` is
created.

| Passport field | Status | Evidence / linked section |
|---|---|---|
| Source materials |  |  |
| Module activation |  |  |
| Resource identity |  |  |
| Parameter authority |  |  |
| QC gates |  |  |
| Local validation |  |  |
| Safety/governance |  |  |
| Unresolved gaps |  |  |
| Validator status |  |  |

## 22. Original-to-revised mapping

| Original section/step | Preserved | Modified | Removed | Added | Reason | Revised SOP section |
|---|---:|---:|---:|---:|---|---|

## 23. Execution blockers before use

| Priority | Required change | Reason | Completion criterion |
|---:|---|---|---|

## 24. Review-to-SOP mapping

| Review finding | Revised_Protocol.md section | Revision action | Status |
|---|---|---|---|

## 25. Red-line self-audit

| Gate | Pass/Fail | Evidence |
|---|---|---|
| No unsupported operational assumptions presented as facts |  |  |
| No vague execution language left unresolved |  |  |
| User-supplied corpus screened before external recommendations |  |  |
| Protocol Readiness Contract locked before SOP rewrite |  |  |
| Parameter authority preserved for recommendations and unresolved gaps |  |  |
| Readout contracts map claims to QC gates |  |  |
| Cross-skill claim-readout handoff completed when claim context exists |  |  |
| Protocol panel synthesis completed before readiness scoring |  |  |
| Data repository/accession placeholders not invented |  |  |
| Critical/Major issues use full logic chain |  |  |
| Evidence sources include exact identity |  |  |
| Companion-derived evidence is resolved or marked for verification |  |  |
| SOP-first structure preserved |  |  |
| Operator burden justified |  |  |
| Validator checks completed or limitation stated |  |  |
