# Data Records and Repository Gate

Use for protocols that produce reusable data, especially scRNA-seq, scATAC-seq,
multiome, methylation, spatial omics, flow cytometry, imaging, proteomics,
metabolomics, sequencing libraries, high-content screening, behavior, or
computational analysis outputs.

## Data record gate

| Output | Raw data | Processed data | Metadata | Repository | Identifier | QC file | Retention |
|---|---|---|---|---|---|---|---|

For every reusable output, require:

- raw data format;
- processed matrix/table/image/plot format;
- sample metadata fields;
- reagent, instrument, software, and pipeline versions;
- reference genome, annotation, database, library, or model version;
- QC metrics and pass/fail thresholds;
- exclusion criteria and disposition;
- repository and accession plan;
- data dictionary or README;
- checksum, backup, or storage-location record where feasible.

## Repository authority

- Do not invent DOIs, accession numbers, repository names, licenses, embargo
  dates, or ethics approvals.
- If accession is not available, write `planned repository / identifier:
  △TO BE CONFIRMED` and state who must confirm it.
- Repository choice must match data type, consent/ethics restrictions, and field
  norms.
- Restricted data require an access route, metadata plan, and governance note.

## Data Records Appendix

For publication-facing SOPs, add a compact appendix or table covering:

| Dataset | Data level | File format | Metadata fields | QC metrics | Repository/access route | Citation/identifier status |
|---|---|---|---|---|---|---|
