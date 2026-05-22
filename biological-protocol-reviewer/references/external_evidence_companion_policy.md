# External Evidence Companion Policy

This policy governs optional external skills, official plugins, MCP tools, and
host-provided capabilities that may support Biological Protocol Reviewer.

This skill remains a single protocol-review and SOP-rewriting skill. Do not
delegate protocol-readiness judgment or SOP authorship to another skill.

External companions may provide:

- public biological context;
- entity normalization;
- literature or database discovery;
- public dataset lookup;
- protocol corpus integrity and source consistency checks;
- downstream bioinformatics handoff information;
- source identifiers;
- output formatting or presentation support after the review is complete.

External companions must not replace:

- protocol reconstruction;
- module activation;
- failure-mode analysis;
- safety/governance red-line review;
- readiness scoring;
- SOP parameter provenance;
- local validation;
- QC gate design;
- stop/go criteria;
- final executable SOP responsibility.

## Invocation rule

Use this file only when companion skills, official plugins, MCP tools, or host
capabilities are installed, enabled, or visibly exposed by the current host, or
when the user asks for external evidence support.

Before using a companion:

1. Confirm it is available in the current host.
2. Define a bounded evidence, source-lookup, analysis-handoff, or output task.
3. Do not send confidential protocols, private data, patient data, private
   sequences, unpublished methods, credentials, or local paths to networked
   tools without explicit user approval.
4. Do not claim a companion was used unless it returned concrete evidence,
   identifiers, artifacts, checks, or outputs.
5. Convert every companion result that affects execution back into the
   biological-protocol-reviewer evidence hierarchy and local-validation rules.

## Evidence hierarchy rule

A companion output is not itself Grade A-C evidence. It can become useful only
when it points to a concrete source identity that satisfies the Grade A-C rules
in `evidence_benchmarking_workflow.md`.

Use companion-derived information as:

- a search route;
- an entity normalization aid;
- a public database context record;
- a pointer to a primary protocol, reporting standard, vendor manual,
  repository record, instrument manual, or core-facility SOP.

Do not convert companion summaries directly into executable SOP parameters. Any
database-derived or companion-derived suggestion that affects execution must be
marked `★RECOMMENDED — TO BE VERIFIED LOCALLY`, `△TO BE CONFIRMED`, or
`TO BE VERIFIED BEFORE EXECUTION` unless supported by a primary protocol,
official standard, vendor or instrument manual, core-facility SOP, or documented
local validation.

## Official Life Science Research plugin / skill

Use the official ChatGPT Life Science Research plugin/skill only when visible in
the current host.

Use for:

- gene, protein, compound, variant, disease, pathway, marker, or dataset
  context;
- public expression, cell-type, and tissue context;
- public omics study discovery;
- target, compound, or variant background;
- public preprint or study discovery;
- biological rationale for a readout, marker, perturbation, or endpoint.

Do not use as sole authority for:

- executable SOP parameters;
- reagent concentrations;
- antibody dilution;
- enzyme amount;
- PCR cycling;
- animal dosing;
- viral titer;
- sequencing depth;
- centrifugation conditions;
- FACS gating thresholds;
- safety requirements;
- clinical decisions.

## Literature and database lookup companions

Use `$paper-lookup`, `$database-lookup`, `$literature-review`,
`$scientific-critical-thinking`, `$scholar-evaluation`, or equivalent lookup and
cross-check companions only when installed and visible.

Use for:

- finding primary protocol papers;
- locating top-journal Methods, STAR Methods, Extended Methods, or Supplementary
  Methods;
- checking official reporting standards;
- identifying vendor manuals, datasheets, RRIDs, accession records, repository
  requirements, and dynamic standards;
- cross-checking whether a recommendation is a source-backed execution need,
  a local-validation need, or only contextual rationale.

Bring back:

- full source title;
- DOI, PMID, official URL, manual version, standard version, vendor document ID,
  accession, RRID, or repository identifier;
- access date for dynamic web/manual sources;
- exact parameter, QC gate, control, metadata field, or reporting requirement
  supported;
- whether the source supports an original-protocol fact, reviewer
  recommendation, or local-validation requirement.

## Academic Research Pipeline / Integrity Companions

Use installed skills or plugin capabilities from
`Imbad0202/academic-research-skills` or equivalent academic-pipeline companions
only when they are visible in the current host or when the user explicitly asks
to use them. Treat them as corpus, integrity, revision-traceability, and passport
companions, not as protocol-readiness authorities.

Use for:

- screening user-supplied SOPs, manuals, datasheets, lab notes, prior revisions,
  or article corpora before external recommendations;
- no-silent-skip corpus logs and exclusion reasons;
- source-consistency checks between protocol text, tables, datasheets,
  repository records, and manuscript methods;
- protocol/passport resumability metadata for long or resumed reviews;
- revision traceability from review issue to SOP change to residual blocker;
- citation and data-availability integrity checks after readiness judgment.

Do not use for:

- final protocol-readiness score;
- SOP authorship;
- changing parameter authority or local validation status;
- replacing biological-protocol-reviewer safety/governance red-line review;
- converting companion summaries directly into executable parameters;
- sending confidential protocols, private data, unpublished methods, local
  paths, credentials, or personal information to a networked service without
  explicit user approval.

Minimum record to bring back:

```text
ARS companion or command:
Companion class: corpus / passport / integrity / citation / revision / output
Input protocol material handled:
Returned artifact or identifier:
Protocol section, source, parameter, or revision affected:
Evidence role: supports / weakens / narrows / flags / context / search_route
Limitation and data-access level:
Local validation status:
```

## Bioinformatics workflow companions

Use GPTomics/bioSkills or equivalent bioinformatics workflow skills only for
downstream analysis handoff and omics-protocol QC context.

Use for:

- raw-data manifest expectations;
- sequencing/read-structure metadata;
- reference genome or database version requirements;
- assay-specific QC metrics;
- batch, lane, index, and sample-balance expectations;
- single-cell, spatial, ATAC, methylation, TCR/BCR, ChIP/CUT&Tag, multiome,
  proteomics, metabolomics, or variant-analysis handoff;
- repository and FAIR metadata planning.

Do not use for:

- wet-lab parameter authority;
- sample-processing parameters unless supported by primary protocol, vendor,
  instrument, or core SOP evidence;
- replacing local validation;
- final SOP readiness scoring.

## Writing, publication, and presentation companions

Use nature-skills, guizang-ppt-skill, open-design, taste-skill, or equivalent
output skills only after `Review_Report.md` and `Revised_Protocol.md` are
scientifically and operationally complete, or when the user explicitly asks for
output conversion.

Use for:

- Nature Protocol-style formatting after evidence review;
- publication-facing methods prose;
- SOP training slides;
- graphical protocol summaries;
- lab-meeting decks;
- visual troubleshooting guides.

Do not use for:

- changing executable parameters;
- weakening safety/governance language;
- removing QC gates;
- replacing source identity;
- changing readiness score.

## Rigorous-Reviewer boundary

Use Rigorous-Reviewer only when the user asks whether protocol-derived evidence
supports a manuscript, proposal, preprint, figure set, dataset, or central
scientific claim.

Do not use Rigorous-Reviewer for SOP authorship, protocol-readiness scoring,
bench-step rewriting, reagent setup, QC release design, safety/governance
red-line decisions, or local-validation planning inside this skill.

## Companion / MCP conflict rules

If both a companion skill and an MCP/tool capability can perform a similar
action, choose the narrower and more auditable route.

- Use companion skills for domain workflow logic, critique structure, analysis
  planning, and output transformation.
- Use MCP tools for concrete retrieval, parsing, computation, file access,
  database access, source verification, and validation.
- Do not call multiple overlapping companions for the same subtask unless the
  user asks for independent cross-checking.
- Do not send confidential protocols, private data, patient data, private
  sequences, unpublished methods, credentials, or local paths to networked tools
  without explicit user approval.
- Record provenance for every external result used.
- Biological Protocol Reviewer remains responsible for final SOP judgment.

## Minimum provenance record

When a companion result is used, record:

```text
Companion/tool used:
Companion class:
Query/entity/task:
Returned source or identifier:
Primary source or official record resolved:
Evidence role: supports / weakens / narrows / neutral / context / search_route
Protocol section affected:
Exact parameter/control/QC/metadata field affected:
Access date, when applicable:
Local validation status:
Limitation / verification needed:
```

If the source cannot be resolved, mark the recommendation as `△TO BE CONFIRMED`
or `TO BE VERIFIED BEFORE EXECUTION`.

## Final report disclosure

If companion skills, plugins, or MCP tools were used, include the optional
`External Evidence Companion Results` table in `Review_Report.md`. Keep detailed
companion/tool audit information out of the bench-facing SOP main body; put it
in parameter provenance or appendices only when needed.

If no companions were used, omit this section unless relevant to explain a
limitation.
