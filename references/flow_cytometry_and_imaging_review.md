# Flow Cytometry and Imaging Review Module

## Flow cytometry audit

- Define tissue digestion, cell recovery, viability, blocking, staining buffer,
  antibody clone, fluorophore, lot, concentration, titration, and incubation.
- Check fluorophore-panel feasibility: brightness, antigen density, spectral overlap,
  autofluorescence, tandem-dye stability, fixation compatibility, and instrument
  configuration.
- Require compensation or spectral unmixing controls, FMO controls for key gates,
  viability dye, doublet exclusion, dump channel logic, and gating hierarchy.
- Require sample acquisition thresholds, event counts, sorting purity mode, post-sort
  purity check, index sorting when needed, and downstream handling.

## Imaging audit

- Define fixation, permeabilization, blocking, antibody validation, mounting,
  exposure, laser power, detector gain, tile/stitch settings, z-step, and objective.
- Check segmentation algorithm, thresholding, background correction, blinded analysis,
  field selection, sampling unit, and quantitative readout.
- Require negative, secondary-only, positive tissue/cell, and autofluorescence
  controls where relevant.

## Common fatal flaws

- No FMO control for a dim or continuous marker used to define a key population.
- No viability/doublet exclusion before rare-cell quantification or sorting.
- Using a bright fluorophore on a high-expression marker while assigning a weak
  fluorophore to a low-expression marker.
- No post-sort purity or viability check when sorted cells drive downstream omics.
- Unblinded image field selection.
