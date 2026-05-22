# Biological Protocol Reviewer

[English version](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Standard-Agent_Skills-blueviolet.svg)](https://agentskills.io/specification)
[![Version](https://img.shields.io/badge/Version-v1.3.3-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.10--3.12-3776AB.svg)](#校验方式)
[![Works with](https://img.shields.io/badge/Works_with-Codex-blue.svg)](#安装方式)

**biological-protocol-reviewer** 是一个用于生物实验 protocol 严格评审和 SOP 重写的 Codex skill。它面向动物、细胞、分子生物学、流式/成像、组学、统计复现性、安全治理和前沿实验方法，目标不是润色文字，而是判断 protocol 是否能被安全执行、正确解释、稳定复现、完整审计，并把不完整 bench notes 改写成有证据支撑的可执行 SOP。


## 默认输出

默认生成两个用户可见文件：

- `Review_Report.md`：protocol 重建、readiness score、Level 0-3 成熟度门槛、模块激活表、证据对标表、按严重性排序的问题块、假设台账、参数溯源、操作者负担预算、mini-pilot 方案，以及 review-to-SOP 映射。
- `Revised_Protocol.md`：面向 bench 的 Markdown SOP，包括快速执行摘要、开始前准备、编号步骤、试剂配制、资源/设备/软件/引物/抗体表、QC gate、疑难排查、预期结果、最小数据分析和审计附录。

这个 skill 不把 protocol 审核当作 copyediting。它首先问：这个流程能否执行、解释、复现、审计，并符合安全和治理要求。

## 结构化资源与校验

需要，但不应该照搬论文评审 skill 的 JSON 逻辑。`rigorous-science-reviewer` 的 JSON 主要服务于论文评分、同行评审问题块和文献检索提示；protocol reviewer 更需要约束的是 **执行成熟度、SOP 可操作性、参数溯源、QC/controls、资源身份、安全治理和本地验证**。

本仓库已经补充多类结构化资源：

- `references/protocol_rubric.json`：规范 readiness score、Level 0-3 成熟度、评分权重、严重性定义和执行前门槛。
- `templates/issue_block_templates.json`：规范 Critical/Major/Minor/Optimization 问题块，强制包含具体问题、证据、影响、failure mode、解决方案、决定性 readout 和 SOP 修订位置。
- `templates/source_search_hints.json`：规范证据检索路径，避免只写“查文献”或“加 controls”，而是把每个参数、控制、QC、资源身份、动态标准和安全治理要求映射到可验证来源。
- `schemas/*.schema.json`：约束结构化 Review_Report、Revised_Protocol、issue、QC gate、parameter provenance、bioinformatics handoff 和可选 external companion evidence。
- `scripts/lint_structured_protocol.py`、`tests/`、`.github/workflows/` 和 `benchmarks/v1.0/`：为 Markdown validator 外再提供确定性回归检查。

Markdown 仍然承载领域规则和 SOP 写作规范；JSON 用来固定重复输出结构，减少不同轮次之间的格式漂移。


## 可选 companion 生态

Biological Protocol Reviewer 可以在当前 host 已暴露相关能力时使用外部 skills、官方 plugins、MCP tools 或 host-provided capabilities。它们只能作为证据发现、来源定位、下游分析交接或输出转换辅助，不能替代 protocol-readiness judgment、SOP 写作责任、安全/治理审查、QC 设计或本地验证。

推荐 companion：

- ChatGPT Life Science Research：公共生物学背景、实体标准化和数据库证据。
- K-Dense-AI/scientific-agent-skills：通过 `$paper-lookup`、`$database-lookup`、`$literature-review`、`$scientific-critical-thinking`、`$scholar-evaluation` 等做文献、数据库、来源和标准检索。
- GPTomics/bioSkills：组学下游分析 handoff、QC metadata、repository planning 和 pipeline expectations。
- Yuan1z0825/nature-skills：readiness review 完成后的 publication-style protocol writing。
- guizang-ppt-skill / open-design / taste-skill：结论固定后的 SOP training deck、visual protocol summary 或展示材料。
- Rigorous-Reviewer：仅用于评估 protocol-derived evidence 是否支撑 manuscript、proposal 或 central scientific claim。

所有 companion 输出都必须解析回具体 source identity，才能支撑 SOP 参数、controls、QC gates、metadata 或 reporting requirements。无法解析来源的 companion-derived 建议必须标记为 `△TO BE CONFIRMED` 或 `TO BE VERIFIED BEFORE EXECUTION`。

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
├── biological-protocol-reviewer/        # 可安装的 Agent Skill 目录
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── references/
│   │   ├── protocol_rubric.json
│   │   ├── skill_manifest.json
│   │   ├── module_activation_and_routing.md
│   │   ├── evidence_benchmarking_workflow.md
│   │   ├── evidence_and_standards_hard_gates.md
│   │   ├── external_evidence_companion_policy.md
│   │   ├── risk_classification_and_redlines.md
│   │   └── output_qc_linter.md
│   ├── templates/
│   │   ├── Review_Report_template.md
│   │   ├── Revised_Protocol_md_structure.md
│   │   ├── issue_block_templates.json
│   │   └── source_search_hints.json
│   ├── schemas/
│   │   ├── review_report.schema.json
│   │   ├── revised_protocol.schema.json
│   │   ├── issue.schema.json
│   │   ├── qc_gate.schema.json
│   │   ├── parameter_provenance.schema.json
│   │   ├── bioinformatics_handoff.schema.json
│   │   └── external_companion_evidence.schema.json
│   ├── scripts/
│   │   ├── protocol_output_validator.py
│   │   ├── lint_structured_protocol.py
│   │   ├── check_installable_skill.py
│   │   ├── check_version_consistency.py
│   │   └── run_regression_fixtures.py
│   └── examples/
│       └── cdh5_ai14_protocol_review_example.md
├── tests/
├── benchmarks/
│   └── v1.0/
├── tools/
│   └── score_protocol_benchmark.py
├── .github/
│   └── workflows/
│       └── validate.yml
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── pyproject.toml
└── LICENSE
```

GitHub 发布用的 README、CHANGELOG、LICENSE、CI、tests 和 benchmark definitions
保留在仓库根目录。真正可安装的 skill 被隔离在
`biological-protocol-reviewer/` 子目录内，避免把仓库维护文件混入运行时包。

## 安装方式

从 GitHub 安装时应使用子路径 `biological-protocol-reviewer`。本地安装时，Codex
解析到的 skill 路径应指向：

```text
<repo-root>/biological-protocol-reviewer
```

不要把仓库根目录直接作为 skill 目录安装，因为根目录包含 GitHub 文档。

## 核心流程

1. 重建 protocol 的 intended result、primary readout、experimental unit、decisive QC gate、最脆弱步骤和可支持结论。
2. 做内部模块路由：动物、细胞、分子、流式/成像、组学、统计复现性、安全治理、frontier methods、材料设备、数据记录、操作者负担和 mini-pilot。
3. 建立证据 dossier，区分原 protocol 事实、外部 benchmark、推荐参数、本地假设、未解决缺口和可选 companion-derived source leads。
4. 外部 companion 只能用于 evidence discovery、source identity、downstream-analysis handoff 或 output conversion，不能外包 SOP 判断。
5. 用 peer-reviewed protocol、top-journal methods、official standards、vendor/instrument manuals、core-facility SOP 和 local validation 对标参数、控制和 QC。
6. 执行安全和治理红线检查。
7. 用 `references/protocol_rubric.json` 和 `templates/issue_block_templates.json` 分配严重性并写完整问题块。
8. 改写为 SOP-first Markdown：bench-critical 内容放主文，设计理由、治理、记录、证据来源、假设和参数溯源放附录。
9. 运行 linter、checklist 和可执行 validator。

## 校验方式

当输出文件存在时运行：

```bash
python3 biological-protocol-reviewer/scripts/protocol_output_validator.py --report Review_Report.md --protocol Revised_Protocol.md
```

该 validator 检查 Review_Report 和 Revised_Protocol.md 的必需结构、章节顺序、未解决模糊语言，以及推荐参数是否缺少参数溯源。它不能替代科学判断。

当需要结构化 JSON 审计提取或回归测试 fixture 时运行：

```bash
python3 biological-protocol-reviewer/scripts/lint_structured_protocol.py tests/fixtures/structured/valid_review_report.json
python3 biological-protocol-reviewer/scripts/lint_structured_protocol.py Revised_Protocol.structured.json --schema biological-protocol-reviewer/schemas/revised_protocol.schema.json
```

维护仓库时运行确定性测试和 benchmark 定义检查：

```bash
python3 biological-protocol-reviewer/scripts/check_installable_skill.py --skill-dir biological-protocol-reviewer
python3 biological-protocol-reviewer/scripts/check_version_consistency.py
python3 biological-protocol-reviewer/scripts/run_regression_fixtures.py
python3 -m unittest discover -s tests -v
python3 tools/score_protocol_benchmark.py --benchmark-root benchmarks/v1.0
```

GitHub Actions 会在 push 和 pull request 时运行同一组检查。版本化 benchmark
在 CI 中只校验定义结构；真实模型输出评分更适合作为 release 前评估门槛，而不是每次提交都自动调用模型。

## 安全边界

当上下文支持合规研究时，本 skill 默认用户是在有资质机构内由受训人员执行合法实验。若请求涉及规避监管、隐瞒偏差或不良事件、非实验室执行受监管工作，或有害生物因子的创建/优化/武器化，则只提供非操作性的治理和安全建议。

## 典型输入

```text
请使用 biological-protocol-reviewer 审核并重写这个 protocol。

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
