# Operator burden budget and mini-pilot validation

Use this reference for every protocol rewrite. The goal is high-quality data without unnecessary work for the operator.

## Operator burden budget

Every added field, control, record, or QC step must map to at least one of:

- Prevents a likely failure mode.
- Protects interpretability of the primary readout.
- Is required by safety, ethics, biosafety, animal welfare, human-subjects, or core-facility governance.
- Is required by a domain reporting or metadata standard.
- Enables batch traceability, repeatability, or data reanalysis.
- Enables a stop/go, rescue/repeat, or exclusion decision.

If a requested field does not satisfy one of these, move it to an optional appendix, combine it with an existing record, or omit it.

## Main-body versus appendix rule

Place in the main SOP body only what the operator needs during execution:

- Start conditions and inputs.
- Procedure steps.
- Reagent setup.
- Resource and instrument setup.
- Critical safety warnings.
- QC gates and fail actions.
- Timing, pause points, troubleshooting, and expected results.

Place in appendices:

- Full governance records.
- Detailed reporting checklists.
- Long metadata forms.
- Literature rationale.
- Assumption ledger and parameter provenance.
- Raw-data manifest and batch records.

## Mini-pilot requirement

When the protocol introduces new reagents, new instruments, new sample types, scaled volumes, substituted kits, antibody panels, primer sets, sequencing/library changes, or unvalidated recommended parameters, add a minimal local-validation mini-pilot.

The mini-pilot must specify:

| Field | Requirement |
|---|---|
| Purpose | What uncertainty the pilot resolves |
| Minimum design | Smallest defensible test, including positive and negative controls |
| Acceptance threshold | Quantitative or categorical pass criterion |
| Stop/go rule | Continue, repeat, rescue, redesign, or exclude |
| Failure interpretation | What conclusion becomes unsupported if it fails |
| Burden control | Why this is the smallest sufficient validation |

## Repeat, rescue, and exclusion rules

For each major QC gate, state:

- Can the run be rescued?
- If yes, what exact rescue action is allowed?
- When must the run be repeated?
- When must a sample be excluded?
- Who approves the exclusion or deviation?

## Burden score

Assign a short burden note in `Review_Report.md`:

| Added requirement | Burden | Value | Keep/appendix/omit decision |
|---|---|---|---|

Use categories: `low`, `moderate`, `high`. High-burden additions require explicit justification.
