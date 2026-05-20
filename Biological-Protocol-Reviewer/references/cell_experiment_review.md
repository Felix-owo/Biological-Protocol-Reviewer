# Cell Experiment Review Module

## Core questions

- What is the biological replicate: donor, mouse, independent culture, clone,
  differentiation batch, organoid line, or plate?
- Are cell identity, source, authentication, mycoplasma status, passage number, and
  culture history specified?
- Are density, confluency, medium, serum lot, matrix, oxygen, CO2, temperature,
  vessel format, feeding schedule, and differentiation state controlled?
- Are treatment vehicle, dose range, exposure time, washout, cytotoxicity, and target
  engagement measured?
- Are transfection/transduction efficiency, multiplicity, selection, editing rate,
  knockdown/knockout validation, and off-target risks addressed?
- Are batch effects from passage, donor, plate position, operator, reagent lot, and
  incubator controlled?

## Required controls

- Untreated and vehicle controls.
- Mock transfection/transduction control.
- Non-targeting guide/siRNA/shRNA or empty-vector control.
- Positive perturbation control when assay responsiveness is uncertain.
- Viability/cell-number normalization for functional assays.
- Mycoplasma-negative documentation and recent authentication for cell lines.

## Common fatal flaws

- Calling technical wells biological replicates.
- Missing vehicle control when solvent/hormone/drug concentration differs.
- No authentication or passage tracking for cell lines.
- No cytotoxicity assessment for expression, reporter, or drug effects.
- Comparing different treatment groups across different culture batches without
  balanced batch layout.
