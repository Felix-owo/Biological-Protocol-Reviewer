# Agent Behavior Core: Scope Discipline, Anti-Slop, and Verification

Use this reference at activation and before final delivery. It defines host-agnostic behavior constraints for Codex, Claude Code, Cursor, Gemini CLI, and other agent runtimes.

## 1. Task reconstruction before output

Before generating review or SOP content, reconstruct:

| Field | Required action |
|---|---|
| User request | State the exact requested artifact and scope. |
| Protocol objective | State intended result and primary readout. |
| Decisive missing material | List missing items that change readiness or execution. |
| Assumptions | Record assumptions; do not convert assumptions into facts. |
| Output boundary | Do not add modules, deliverables, or literature digressions that do not change protocol readiness. |

## 2. Surgical output discipline

Every issue, SOP edit, QC gate, control, record field, mini-pilot requirement, or safety/governance note must trace to at least one of:

- a user-supplied protocol step, reagent, sample, instrument setting, readout, or stated goal;
- a concrete failure mode affecting execution, interpretation, safety, reproducibility, or auditability;
- a Grade A-C source, official standard, vendor manual, or local validated SOP;
- an explicit unresolved parameter or resource-identity gap;
- a required deliverable requested by the user.

Remove generic content that cannot be traced to one of these anchors.

## 3. Anti-overengineering gate

Do not add complexity unless it changes a decision, prevents a plausible failure mode, satisfies governance, or is needed for auditability.

Forbidden unless explicitly justified:

- broad literature summaries not tied to a protocol decision;
- controls that do not map to a named failure mode;
- metadata tables that duplicate existing records;
- speculative modules unrelated to the supplied protocol;
- long audit appendices that bury bench-critical instructions;
- parameter values without source identity and local-validation status.

## 4. No-faux-precision rule

Do not invent catalog numbers, clones, RRIDs, primer/oligo sequences, gRNA sequences, barcode structures, accession IDs, software versions, instrument settings, sequencing depths, centrifugation parameters, incubation times, concentrations, dosages, thresholds, PMIDs, DOIs, or manual versions.

Use:

- `△TO BE CONFIRMED` when a value cannot be responsibly inferred;
- `★RECOMMENDED — TO BE VERIFIED LOCALLY` when a source-supported value lacks local validation.

## 5. Assumption ledger

When assumptions affect readiness, use:

| ID | Assumption | Why needed | Risk if false | How to verify | SOP/report impact |
|---|---|---|---|---|---|

## 6. Verification contract

When creating or revising files, report:

- files changed or created;
- validators/tests run;
- exit status;
- unresolved failures;
- limitations of validation.

If validation cannot be run, state why and downgrade confidence.
