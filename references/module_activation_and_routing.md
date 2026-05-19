# Module Activation and Routing Rules

This skill must remain a single skill. Do not delegate to separate skills. Instead, perform an internal module-routing step at the beginning of every protocol review and document the selected modules in `Review_Report.md`.

## Required routing pass

Before benchmarking or rewriting, scan the supplied protocol for experimental objects, procedures, reagents, instruments, analysis endpoints, and regulatory constraints. Activate every relevant module; modules are not mutually exclusive.

## Routing table

| Module | Activate if the protocol contains | Required outputs in review | Required insertions in revised DOCX |
|---|---|---|---|
| Animal experiments | mouse, rat, zebrafish, animal model, surgery, injection, gavage, anesthesia, euthanasia, tissue harvest, genotype, breeding, IACUC | animal welfare audit, ARRIVE/PREPARE gaps, randomization/blinding/sample-size review, humane endpoints, analgesia/anesthesia/welfare records | animal provenance table, procedure authorization placeholders, welfare monitoring, anesthesia/analgesia records, endpoint criteria, tissue harvest metadata |
| Cell experiments | cell culture, primary cells, organoids, cell lines, transfection, infection, perturbation, differentiation, viability, sorting after culture | authentication/mycoplasma/passage audit, cell density/confluency audit, treatment design, contamination risk, batch effect risk | cell provenance table, culture metadata, authentication and mycoplasma records, passage limits, density/confluency targets, treatment records |
| Molecular biology | PCR, RT, qPCR, cloning, enzyme reaction, ligation, tagmentation, library pre-amplification, gel, beads, cleanup, nucleic acid extraction | primer/oligo audit, enzyme/buffer compatibility, input/yield/QC audit, contamination controls, MIQE if qPCR | master-mix recipes, cycling programs, cleanup ratios, nucleic-acid QC gates, no-template/no-RT/positive controls, primer table |
| Flow cytometry and imaging | FACS, flow cytometry, cell sorting, antibody panel, fluorophore, compensation, spectral unmixing, microscopy, IF/IHC, confocal, image analysis | panel conflict table, antibody clone/RRID audit, control completeness, gating/imaging analysis critique, instrument metadata gaps | antibody titration plan, FMO/single-stain/unstained controls, compensation/unmixing procedure, gating appendix, sort purity/viability QC, imaging settings |
| Omics | bulk RNA-seq, scRNA-seq, ATAC-seq, methylation, multiome, WGBS/RRBS, CUT&Tag, ChIP-seq, library prep, sequencing, demultiplexing, barcode, UMI | library design audit, input and complexity review, batch design, sequencing depth, metadata/repository requirements, computational QC | library QC gates, index/barcode plan, pooling and sequencing plan, raw-data manifest, analysis metadata, repository checklist |
| Statistics and reproducibility | any comparative experiment, quantitative endpoint, group design, screening, omics, imaging quantification, flow quantification | experimental unit, n, power/rationale, randomization, blinding, exclusion, replicate structure, batch effect and statistical test review | study-design table, randomization/blinding/exclusion records, statistical analysis plan, replicate definitions, batch/blocking metadata |
| Safety/governance | hazardous chemical, recombinant DNA, viral vector, human-derived material, animal work, sharps, lasers, controlled equipment, regulated material | approval gap review, PPE/waste/decontamination audit, facility authorization, incident/deviation handling | approval ID placeholders, training records, PPE, waste disposal, decontamination, emergency/deviation forms |
| Frontier methods | CRISPR/base editing/prime editing, perturb-seq, pooled screens, viral vectors, organoids/co-culture, single-cell multiome, spatial omics, proteomics/metabolomics, high-content imaging, animal surgery/behavior | activate the relevant frontier submodule, require method-specific controls/QC, batch-effect review, mini-pilot if transferred or unvalidated | method-specific metadata, validation plan, stop/go gates, resource identity, software/reference versions |

## Module activation output

Add the following table to `Review_Report.md`:

| Module | Status | Triggering evidence from protocol | Main risk if omitted | Reference file used |
|---|---|---|---|---|

Use statuses:
- `Activated`
- `Not activated — not applicable`
- `Unclear — needs confirmation`

## Conflict rule

If modules conflict, use the stricter requirement. For example, a single-cell FACS-sorted animal protocol must satisfy animal, flow, molecular/omics, statistics, data-record, and governance requirements simultaneously.

## Frontier method routing

When `Frontier methods` is activated, read `references/frontier_method_modules.md` and include each selected submodule in the module activation table. Do not treat frontier methods as optional polish; they often define the decisive controls, QC gates, metadata, and batch-effect safeguards.

## Missing-context rule

If the protocol implies a module but lacks enough detail, activate the module anyway and mark the missing information as `△TO BE CONFIRMED` or `TO BE COMPLETED BEFORE EXECUTION`.
