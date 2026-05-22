# Readout Contract

Use before defining controls, QC gates, anticipated results, release criteria,
or interpretation boundaries. Every readout must defend a specific conclusion,
not merely produce a measurement.

## Per-readout contract

| Field | Required content |
|---|---|
| Readout ID | Stable ID used in review report and SOP. |
| Conclusion supported | Biological or technical conclusion the readout can support. |
| Sample/experimental unit | Unit used for pass/fail and interpretation. |
| Positive control | Result proving the system can detect a true signal. |
| Negative/control readout | Result defining background, contamination, specificity, or baseline. |
| Failure modes detected | What can make the run uninterpretable. |
| Acceptance criterion | Quantitative or categorical release threshold. |
| Fail action | Stop, rescue, repeat, exclude, downgrade, or flag for PI/core review. |
| Interpretation boundary | What cannot be concluded even if the readout passes. |
| Record field | Where the observed value is recorded. |

## Rules

- Do not write generic "include QC" language; name the failure mode and release
  criterion.
- A readout with no positive or negative/control comparator cannot support a
  strong interpretive claim.
- If the readout is destructive, rare, expensive, animal-dependent, or
  sequencing-dependent, add a stop/go decision before irreversible steps where
  feasible.
- If the readout supports publication or reusable data, link it to the data
  record and repository gate.
