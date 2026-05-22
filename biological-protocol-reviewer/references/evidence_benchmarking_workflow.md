# Evidence Benchmarking Workflow

Use this workflow before assigning severity or rewriting operational parameters. Also apply `references/evidence_and_standards_hard_gates.md`.

## 1. Classify the protocol class

Assign one or more classes:
- animal intervention or tissue collection
- cell culture or cell perturbation
- molecular biology assay
- flow cytometry, sorting, or imaging
- sequencing or other omics assay
- computational/statistical analysis linked to wet-lab endpoints
- mixed multi-module protocol

## 2. Search and evidence hierarchy

Use sources in this priority order:
1. Peer-reviewed protocol papers: Nature Protocols, STAR Protocols, Current Protocols, JoVE, or equivalent detailed protocol venues.
2. Top-journal Methods, STAR Methods, Extended Methods, and Supplementary Methods.
3. Reporting and metadata standards: ARRIVE 2.0, PREPARE, MIQE, MIFlowCyt, MINSEQE, FAIR, ENCODE-style metadata principles, repository submission rules.
4. Official vendor manuals, datasheets, kit handbooks, antibody datasheets, instrument manuals, software documentation.
5. Core-facility or institutional SOPs.
6. Local practice only if explicitly labelled as local validation rather than universal best practice.


## 2.1 Optional external evidence companions

Host-provided plugins, external skills, or MCP tools may help locate sources or
normalize entities, but they do not change the evidence hierarchy.

A companion output is not itself Grade A-C unless it points to a concrete source
identity that satisfies the Grade A-C rules.

Use companion-derived evidence as:

- a search route;
- an entity normalization aid;
- a public database context record;
- a pointer to a primary protocol, reporting standard, vendor manual,
  repository record, instrument manual, or core-facility SOP.

Do not convert companion summaries directly into executable SOP parameters. If a
companion-derived source cannot be resolved, mark the linked recommendation as
`△TO BE CONFIRMED` or `TO BE VERIFIED BEFORE EXECUTION`.

## 3. Evidence grading

| Grade | Meaning | Typical use |
|---|---|---|
| A | Peer-reviewed protocol or formal reporting standard | Strong basis for required controls, reporting fields, and common parameter ranges |
| B | Detailed methods from top-journal paper | Strong basis for assay structure and parameter ranges, but may be study-specific |
| C | Vendor manual, instrument documentation, antibody datasheet, core SOP | Strong basis for kit/instrument-specific execution and QC |
| D | Local practice, inferred parameter, or expert assumption | Use only with explicit local-validation label |

## 3.1 Source identity hard gate

For every Grade A-C benchmark source, record:

- full title or standard/manual name;
- DOI, PMID, official URL, manual version, standard version, or vendor document ID;
- access date for web/manual sources;
- exact parameter, control, QC gate, metadata field, or reporting requirement supported;
- whether the source supports an original-protocol fact, a reviewer recommendation, or a local-validation requirement.

Do not use only broad labels such as `Nature Protocols` or `vendor manual` when a specific source can be identified. If live web access is unavailable for a dynamic standard, label the item `TO BE VERIFIED BEFORE EXECUTION`.

## 4. Parameter decision rules

- If Grade A/B/C sources agree, recommend the convergent parameter and cite its source class.
- If Grade A/B/C sources disagree, report the defensible range, explain why the choice matters, and require local validation.
- If only Grade D evidence exists, write `★RECOMMENDED — TO BE VERIFIED LOCALLY`.
- If no defensible value exists, write `△TO BE CONFIRMED` and specify exactly who or what must confirm it.
- Never present inferred parameters as original-protocol facts.

## 5. Required benchmark table

Every `Review_Report.md` must include:

| Protocol component | Benchmark source identity | Grade | Exact supported parameter/requirement | Original protocol status | Reviewer decision | Access/version |
|---|---|---|---|---|---|---|

Every `Revised_Protocol.md` must include a `Parameter provenance` table when recommended parameters are introduced.

## 6. FAIR and data-quality release gate

For omics, imaging, flow cytometry, and computationally interpreted endpoints, add release criteria for raw-data existence, file naming, software/version, instrument settings, reference/database version, QC metric, storage path, backup status, and checksum or unique file identifier when feasible.
