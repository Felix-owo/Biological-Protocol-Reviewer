# BPR_002_scrna_batch_confounding

## Protocol excerpt

Collect control samples on Monday and treated samples on Friday. Process each
condition with a different library kit lot. Sequence the two conditions on
separate lanes and compare clusters after standard analysis.

## Intended hidden defects

- Condition is completely confounded with processing day.
- Condition is completely confounded with library kit lot.
- Condition is completely confounded with sequencing lane.
- Donor/sample metadata, viability threshold, doublet handling, ambient RNA
  handling, and bioinformatics handoff are absent.
- The protocol lacks a stop/go gate for low-quality libraries.
