# Biological Protocol Reviewer

**Biological-Protocol-Reviewer** 是一个用于生物实验 protocol 严格评审和 SOP 重写的 Codex skill。它面向动物、细胞、分子生物学、流式/成像、组学、统计复现性、安全治理和前沿实验方法，目标不是润色文字，而是判断 protocol 是否能被安全执行、正确解释、稳定复现、完整审计，并把不完整 bench notes 改写成有证据支撑的可执行 SOP。

English version: [README.md](README.md).

## 默认输出

默认生成两个用户可见文件：

- `Review_Report.md`：protocol 重建、readiness score、Level 0-3 成熟度门槛、模块激活表、证据对标表、按严重性排序的问题块、假设台账、参数溯源、操作者负担预算、mini-pilot 方案，以及 review-to-SOP 映射。
- `Revised_Protocol.md`：面向 bench 的 Markdown SOP，包括快速执行摘要、开始前准备、编号步骤、试剂配制、资源/设备/软件/引物/抗体表、QC gate、疑难排查、预期结果、最小数据分析和审计附录。

这个 skill 不把 protocol 审核当作 copyediting。它首先问：这个流程能否执行、解释、复现、审计，并符合安全和治理要求。

## 是否需要像 rigorous-science-reviewer 一样增加 JSON？

需要，但不应该照搬论文评审 skill 的 JSON 逻辑。`rigorous-science-reviewer` 的 JSON 主要服务于论文评分、同行评审问题块和文献检索提示；protocol reviewer 更需要约束的是 **执行成熟度、SOP 可操作性、参数溯源、QC/controls、资源身份、安全治理和本地验证**。

本仓库已经补充三类结构化 JSON：

- `references/protocol_rubric.json`：规范 readiness score、Level 0-3 成熟度、评分权重、严重性定义和执行前门槛。
- `templates/issue_block_templates.json`：规范 Critical/Major/Minor/Optimization 问题块，强制包含具体问题、证据、影响、failure mode、解决方案、决定性 readout 和 SOP 修订位置。
- `templates/source_search_hints.json`：规范证据检索路径，避免只写“查文献”或“加 controls”，而是把每个参数、控制、QC、资源身份、动态标准和安全治理要求映射到可验证来源。

Markdown 仍然承载领域规则和 SOP 写作规范；JSON 用来固定重复输出结构，减少不同轮次之间的格式漂移。

## 证据标准

本 skill 强制记录证据来源的精确身份。常用金标准和动态标准包括：

- 动物实验报告和规划：[ARRIVE 2.0](https://arriveguidelines.org/arrive-guidelines)、[PREPARE](https://norecopa.no/prepare)。
- qPCR/RT-qPCR 报告：MIQE guideline，PMID [19246619](https://pubmed.ncbi.nlm.nih.gov/19246619/)。
- 流式细胞术报告：MIFlowCyt guideline，PMID [18752282](https://pubmed.ncbi.nlm.nih.gov/18752282/)。
- FAIR 数据原则：DOI [10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)。
- 生物安全和重组/合成核酸治理：[NIH Guidelines](https://osp.od.nih.gov/policies/biosafety-and-biosecurity-policy/)、[CDC/NIH BMBL](https://www.cdc.gov/labs/bmbl/index.html)、[WHO Laboratory Biosafety Manual, 4th edition](https://www.who.int/publications/i/item/9789240011311)。
- 资源身份：[RRID portal](https://www.rrids.org/) 和期刊 Key Resources Table 规范，例如 [Cell Press Key Resources Tables](https://www.elsevier.com/en-gb/researcher/author/tools-and-resources/key-resources-table)。

所有 Grade A-C 证据都应记录 DOI、PMID、official URL、manual/standard version、vendor document ID 或 access date。不能编造 catalog number、clone、RRID、序列、剂量、genotyping band、软件版本、阈值或测序深度。

## 仓库结构

```text
.
├── Biological-Protocol-Reviewer/        # 可安装的 Codex skill 目录
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

GitHub 发布用的 README、CHANGELOG 和 LICENSE 保留在仓库根目录。真正可安装的
skill 被隔离在 `Biological-Protocol-Reviewer/` 子目录内，避免把仓库说明文件混入
Codex skill 包。

## 安装方式

从 GitHub 安装时应使用子路径 `Biological-Protocol-Reviewer`。本地安装时，Codex
解析到的 skill 路径应指向：

```text
<repo-root>/Biological-Protocol-Reviewer
```

不要把仓库根目录直接作为 skill 目录安装，因为根目录包含 GitHub 文档。

## 核心流程

1. 重建 protocol 的 intended result、primary readout、experimental unit、decisive QC gate、最脆弱步骤和可支持结论。
2. 做内部模块路由：动物、细胞、分子、流式/成像、组学、统计复现性、安全治理、frontier methods、材料设备、数据记录、操作者负担和 mini-pilot。
3. 建立证据 dossier，区分原 protocol 事实、外部 benchmark、推荐参数、本地假设和未解决缺口。
4. 用 peer-reviewed protocol、top-journal methods、official standards、vendor/instrument manuals、core-facility SOP 和 local validation 对标参数、控制和 QC。
5. 执行安全和治理红线检查。
6. 用 `references/protocol_rubric.json` 和 `templates/issue_block_templates.json` 分配严重性并写完整问题块。
7. 改写为 SOP-first Markdown：bench-critical 内容放主文，设计理由、治理、记录、证据来源、假设和参数溯源放附录。
8. 运行 linter、checklist 和可执行 validator。

## 校验方式

当输出文件存在时运行：

```bash
python3 Biological-Protocol-Reviewer/scripts/protocol_output_validator.py --report Review_Report.md --protocol Revised_Protocol.md
```

该 validator 检查 Review_Report 和 Revised_Protocol.md 的必需结构、章节顺序、未解决模糊语言，以及推荐参数是否缺少参数溯源。它不能替代科学判断。

## 安全边界

当上下文支持合规研究时，本 skill 默认用户是在有资质机构内由受训人员执行合法实验。若请求涉及规避监管、隐瞒偏差或不良事件、非实验室执行受监管工作，或有害生物因子的创建/优化/武器化，则只提供非操作性的治理和安全建议。

## 典型输入

```text
请使用 Biological-Protocol-Reviewer 审核并重写这个 protocol。

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
