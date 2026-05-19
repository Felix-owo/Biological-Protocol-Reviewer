# Statistics and Reproducibility Review Module

## Design audit

- Define experimental unit before sample size and statistics.
- Distinguish biological replicates, technical replicates, repeated measures, and
  subsampling.
- Require sample-size rationale or power/sensitivity logic.
- Check randomization, blinding, allocation concealment, blocking, batch balance,
  and pre-specified exclusion criteria.
- Specify primary endpoint, secondary endpoints, exploratory endpoints, and failure
  criteria before data collection.

## Analysis audit

- Match model to design: mixed models for litter/cage/donor/repeated measures,
  nonparametric or transformation strategy when assumptions fail, multiple-testing
  correction for omics/high-dimensional screens.
- Require effect sizes and uncertainty intervals, not only P values.
- Require versioned software, packages, parameters, seeds, and code/data availability.

## Reproducibility audit

- Can another trained researcher reproduce the protocol using the document alone?
- Are ambiguous values replaced by fixed ranges or acceptance criteria?
- Are deviations logged?
- Are batch, operator, reagent lot, instrument, and software version tracked?
