# SOP Traceability and Change Discipline

Use before and after rewriting `Revised_Protocol.md`. The goal is to prevent the reviewer from turning a protocol review into an uncontrolled rewrite.

## 1. Change authority

Each SOP change must map to one or more of:

| Change authority | Examples |
|---|---|
| User-supplied fact | Original protocol step, reagent, sample, local practice, instrument setting |
| Failure mode | Ambiguous incubation, missing control, untracked batch, unsafe sample handling |
| Readout contract | Positive/negative/process control, acceptance criterion, fail action |
| Parameter authority | Original, local validated, vendor/manual, external benchmark, unresolved gap |
| Safety/governance | Biosafety, ethics, animal welfare, human-subjects, core-facility authorization |
| Auditability | Data record, lot tracking, raw-data manifest, deviation log |

## 2. Required review-to-SOP mapping

`Review_Report.md` should include a concise mapping table:

| Review issue | SOP section changed | Change type | Authority | QC/readout affected | Burden decision |
|---|---|---|---|---|---|

## 3. Change types

Use these labels:

- `clarify` — preserves original action but removes ambiguity;
- `gate` — adds QC/release/fail-action logic;
- `control` — adds control tied to a named failure mode;
- `record` — adds audit or data-record field;
- `safety` — adds required safety/governance condition;
- `parameter-label` — marks a value as original, recommended, or unresolved;
- `move-to-appendix` — removes non-bench material from the main SOP body.

## 4. Forbidden rewrites

Do not:

- convert `△TO BE CONFIRMED` into an executable value;
- convert `★RECOMMENDED — TO BE VERIFIED LOCALLY` into a final local parameter;
- delete user-supplied local constraints without stating why;
- add a control without naming the failure mode it resolves;
- add a high-burden record without operator-burden justification;
- hide safety, exclusion, repeat, rescue, or stop criteria in prose without a clear gate.

## 5. Final check

Before delivery, verify:

- every Critical/Major issue has a SOP mapping or an explicit reason no SOP change can fix it;
- every new QC gate has an acceptance criterion and fail action;
- every recommended/unresolved parameter appears in the parameter-provenance table;
- bench-critical steps remain in the main body, not only in appendices.
