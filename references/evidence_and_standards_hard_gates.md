# Evidence and standards hard gates

Use this reference before scoring protocol maturity or rewriting operational parameters.

## Source identity is mandatory

Every Grade A-C benchmark source must include:

- Full source title or standard name.
- Source type and evidence grade.
- DOI, PMID, official URL, manual version, standard version, or vendor document identifier.
- Access date for web/manual sources.
- Exact parameter, control, metadata field, or reporting requirement supported.

Do not cite only a venue or source class when a concrete source is available.

## Dynamic standards check

Check the current version or official landing page for standards likely to change:

| Topic | Required source type |
|---|---|
| Animal experiments | ARRIVE 2.0 and PREPARE official pages |
| qPCR/RT-qPCR | MIQE guideline paper and any assay-specific update |
| Flow cytometry/sorting | MIFlowCyt plus current core-facility or instrument guidance |
| Omics/sequencing | MINSEQE/FAIR plus platform chemistry and repository metadata |
| Recombinant or synthetic nucleic acids | Current NIH Guidelines official page |
| Biosafety and biohazard work | CDC/NIH BMBL and WHO Laboratory Biosafety Manual official pages |
| Key resources | RRID and Cell Press Key Resources Table guidance |

If live web access is unavailable, state that the standards check is based on local knowledge and mark dynamic guidance as `TO BE VERIFIED BEFORE EXECUTION`.

## FAIR and data-quality release gates

For omics, imaging, flow cytometry, and any computationally interpreted endpoint, add release gates for:

- Raw-data file existence and naming.
- Software and version record.
- Instrument setting record.
- Reference genome/database/library version.
- Processing command or pipeline version.
- QC metric and pass/fail decision.
- Data storage path and backup status.
- Checksum or unique file identifier when feasible.
- Analysis rerun test for publication-grade SOPs.

## Resource identity gate

Key biological and analytical resources must be identified as completely as possible:

- Antibodies: target, clone, fluorophore/conjugate, vendor, catalog number, RRID, lot, titration status.
- Cell lines: source, identifier/RRID, authentication, mycoplasma status, passage range.
- Animals: species, strain, sex, age, source, genotype, housing and approval record.
- Software: name, version, parameters, repository or RRID/DOI when available.
- Kits and instruments: vendor, catalog/model, version, lot/serial/core ID, calibration.

If a key identity field is unknown, the SOP may still be drafted, but the field must be marked `△TO BE CONFIRMED` and execution readiness cannot be Level 3 until the field is resolved or justified as non-critical.
