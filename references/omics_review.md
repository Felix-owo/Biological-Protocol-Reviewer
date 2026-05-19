# Omics Review Module

## Experimental design

- Define biological replicate, technical replicate, batch, lane/run, donor, animal,
  litter, tissue, cell state, and library.
- Balance groups across extraction day, library-prep batch, index set, sequencing
  lane/run, operator, and instrument.
- Specify metadata required for interpretation: genotype, sex, age, tissue, cell type,
  treatment, time, batch, dissociation method, viability, input amount, RIN or
  equivalent quality, and sequencing identifiers.

## Single-cell and single-nucleus omics

Audit:

- Cell/nucleus isolation bias, viability, doublet/multiplet rate, ambient RNA,
  dissociation-induced genes, cell recovery target, loading concentration, and
  low-quality cell thresholds.
- Library complexity, median genes/features, UMI counts, mitochondrial fraction,
  duplication, saturation, mapping rate, exonic/intronic balance, and batch effects.
- Doublet detection, ambient correction, normalization, integration, clustering,
  marker validation, trajectory assumptions, differential abundance, and multiple
  testing.

## DNA methylation / bisulfite / methylome

Audit:

- DNA input, conversion efficiency, spike-in/unmethylated controls, duplication,
  coverage, CpG filtering, conversion artifacts, mapping bias, strand handling,
  allele-specific effects, and region-level statistics.

## Bulk RNA-seq / ATAC-seq / ChIP-CUT&Tag

Audit:

- Input quality, replicate count, library complexity, fragment distribution, mapping,
  duplication, peak metrics, FRiP or enrichment metrics, blacklists, normalization,
  batch correction, covariates, and validation.

## Repository and reproducibility

Require raw data, processed matrices, metadata, code, software versions, reference
genomes, parameters, and accession plan. Use SRA/GEO/ArrayExpress/proteomics
repositories as appropriate.

For Level 3 SOPs, add FAIR/data-quality release gates: raw-data manifest, file
naming, storage path, backup status, checksum or unique file ID when feasible,
instrument/software versions, reference/database versions, and an analysis rerun
test for publication-grade outputs.

## Common fatal flaws

- Batch perfectly confounded with condition.
- Treating cells as independent biological replicates when animals/donors are the
  true biological units.
- No raw data or metadata deposition plan.
- No validation of inferred trajectories, lineage relationships, or cell-state labels.
- Overcorrecting batch effects and erasing true biological contrasts without checks.
