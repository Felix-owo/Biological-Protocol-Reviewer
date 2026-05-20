# Chinese output and Nature Protocols-style formatting standard

## Default language

Unless the user explicitly requests another language, all user-facing outputs must be written primarily in Simplified Chinese.

- `Review_Report.md` must use Chinese headings, Chinese review language, and Chinese severity explanations.
- `Revised_Protocol.docx` must use Chinese as the primary language.
- Technical terms may retain standard English names in parentheses on first use, especially reagent names, instrument settings, antibodies, fluorophores, gene names, software, databases, statistical models, and reporting standards.
- File names should default to Chinese-compatible names unless the user requests English file names. The required canonical outputs remain `Review_Report.md` and `Revised_Protocol.docx`; a Chinese display title may be used inside the documents.

## Nature Protocols-inspired SOP-first document style

The revised protocol must be written in a Nature Protocols-inspired style while remaining directly usable as a bench-facing SOP. Use this as a formatting and editorial target, not as a claim of journal endorsement.

The DOCX must contain these major H1-level sections unless genuinely irrelevant:

1. 标题
2. 文档控制
3. SOP快速执行摘要
4. 开始前准备
5. 实验步骤
6. 试剂配制
7. 试剂、耗材、仪器、引物/oligos、抗体/探针
8. 质量控制与放行标准
9. 时间安排与暂停点
10. 疑难排查
11. 预期结果
12. 数据分析与结果解释
13. 附录A：应用范围、局限性与实验设计
14. 附录B：治理、授权、人员资质、伦理、安全与生物安全
15. 附录C–K：运行记录、批号记录、设备记录、QC、偏差、原始数据、试剂批次、报告清单、假设台账与参数溯源

The procedure must be a numbered list of direct experimental instructions. Each step should use clear active-language commands and defined parameters.
Do not place long background, governance, or reporting-checklist prose before the executable procedure. Keep execution-critical safety and approval checks in the main body, and place full governance and audit records in appendices.

## Required callout symbols

Use the following callout tags consistently throughout `Revised_Protocol.docx`. These tags should appear as visually distinct markers at the start of the relevant sentence or paragraph.

| Tag | Use |
|---|---|
| ▲CRITICAL | A step, parameter, control, acceptance criterion, or handling rule that is essential for success, interpretability, or biosafety. |
| ⚠CAUTION | Hazard, animal welfare issue, biohazard, chemical hazard, sharp hazard, laser hazard, infectious material, or other safety concern. |
| ⏱TIMING | Approximate time required for a section or step block. |
| ⏸PAUSE POINT | A validated place where the protocol can be paused, including exact storage condition and maximum duration. |
| ◉EXPDATE | Expiration date, shelf life, use-by limit, storage condition, freeze-thaw limit, or discard criterion for prepared reagents. |
| ◆QC | Quality-control checkpoint, measurable acceptance criterion, pass/fail decision, or release criterion. |
| ✱TROUBLESHOOTING | Step-linked issue that maps to the troubleshooting table. |
| ⬢RECORD | Data-recording requirement; must map to an appendix table or run sheet. |
| △TO BE CONFIRMED | Parameter, vendor, catalog number, clone, lot, concentration, shelf life, or instrument setting not specified in the source protocol and not safely verifiable. |
| ★RECOMMENDED | Recommended best-available reagent/equipment/parameter when the original protocol omits a required detail; must be marked `RECOMMENDED — TO BE VERIFIED LOCALLY`. |

## Tone and visual style

Use a professional Chinese SOP tone: concise, imperative, audit-ready, and technically exact.

- Avoid conversational language in the DOCX.
- Use tables heavily for reagent setup, resources, equipment, primers/oligos, antibodies/probes, QC, timing, troubleshooting, and records.
- Follow `references/markdown_sop_style.md` for default typography, page geometry, table fills, and color tokens unless the user supplies another DOCX style reference.
- Use consistent typography: clear heading hierarchy, compact tables, and readable spacing.
- Use neutral scientific colors if styling is available: dark blue or charcoal for major headings, light gray table headers, subtle borders. Do not use decorative colors that reduce readability.
- Use bold sparingly for callout tags and acceptance criteria.
- Preserve enough white space so that long SOP tables remain legible.

## Materials and reagent style in Chinese output

The Chinese DOCX must still preserve purchase-ready English identifiers:

- 试剂中文名 / English name
- Vendor / 品牌
- Cat. No. / 货号
- Clone / 克隆号 for antibodies
- RRID when available
- Lot No. / 批号记录栏
- Stock concentration / 母液浓度
- Working concentration / 工作浓度
- Storage / 储存条件
- ◉EXPDATE / 有效期
- Validation status / 验证状态

If a reagent, antibody, kit, consumable, or device is not specified in the original protocol, recommend an optimal option when possible and mark it as:

`★RECOMMENDED — TO BE VERIFIED LOCALLY`

Do not present a recommended choice as if it was supplied by the original protocol.

## Review report style

`Review_Report.md` must be in Chinese by default and use the following severity labels:

- Critical flaw / 致命问题
- Major flaw / 重大问题
- Minor issue / 次要问题
- Optimization / 优化建议

Every critique must map to one or more revised DOCX sections and must state whether the revised protocol corrected the issue, retained it as a locally validated option, or marked it as `△TO BE CONFIRMED`.
