# Assumption Ledger and Parameter Provenance Rules

## Purpose

Separate facts from the original protocol, literature/vendor-derived recommendations, local assumptions, and unresolved gaps.

## Original-to-revised mapping

Both deliverables must preserve traceability between the original protocol and the revised SOP. Add this table to `Review_Report.md`:

| Original section/step | Preserved | Modified | Removed | Added | Reason | Revised Markdown SOP section |
|---|---:|---:|---:|---:|---|---|

## Assumption ledger

Add an assumption ledger whenever the revised protocol fills missing context:

| Assumption | Basis | Risk if wrong | Verification required before execution | Where used |
|---|---|---|---|---|

Rules:
- Do not bury assumptions inside prose.
- Do not label assumptions as validated facts.
- If an assumption affects dose, timing, sample size, endpoint interpretation, biosafety, animal welfare, or library quality, mark it as a Major or Critical issue unless the protocol already contains a validation plan.

## Parameter provenance table

Every recommended or substituted parameter must be tracked:

| Parameter | Original value | Revised value | Provenance | Confidence | Local verification requirement |
|---|---:|---:|---|---|---|

Permitted provenance labels:
- `Original protocol`
- `Peer-reviewed protocol / reporting standard`
- `Top-journal methods`
- `Vendor or instrument manual`
- `Core-facility SOP`
- `Expert recommendation — TO BE VERIFIED LOCALLY`
- `Unknown — TO BE CONFIRMED`

## Labeling rules

- Use `★RECOMMENDED — TO BE VERIFIED LOCALLY` for defensible but not locally validated values.
- Use `△TO BE CONFIRMED` for missing values that cannot be responsibly inferred.
- Use `TO BE COMPLETED BEFORE EXECUTION` for administrative identifiers, approval IDs, training records, instrument booking IDs, lot numbers, and run-specific fields.
