# Molecular Biology Review Module

## Core questions

- Are input material amount, purity, integrity, storage, freeze-thaw count, and
  extraction method defined?
- Are primer/probe sequences, amplicon size, target isoform/genome build, melting
  temperature, specificity, and validation described?
- Are reaction components, final concentrations, enzyme compatibility, buffer,
  additives, cycling conditions, and cleanup ratios unambiguous?
- Are no-template, no-RT, positive-template, extraction blank, spike-in, and
  inhibition controls included where relevant?
- Are expected product size, yield, molarity, fragment distribution, conversion rate,
  duplication rate, and failure thresholds specified?

## qPCR / RT-qPCR

Apply MIQE-style review:

- RNA integrity and quantification method.
- Reverse-transcription priming strategy.
- No-RT and NTC controls.
- Primer efficiency and dynamic range.
- Reference gene validation under the exact experimental condition.
- Cq handling, replicate handling, and outlier rules.

## Library construction

Audit:

- Input amount and minimum quality.
- Adapter/index design and index collision risk.
- PCR cycle number and over-amplification risk.
- Size selection and bead-ratio logic.
- Cleanup carryover.
- Library QC before sequencing.
- Expected insert size and molarity.
- Re-prep criteria.

## Common fatal flaws

- Missing no-template or no-RT controls.
- No expected band/fragment size for genotyping or PCR.
- Ambiguous primer mix concentration.
- No template inhibition check in crude lysates.
- No library over-amplification criteria.
