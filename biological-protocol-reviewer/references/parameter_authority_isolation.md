# Parameter Authority Isolation

Use before accepting, recommending, substituting, or marking any parameter,
reagent, instrument setting, software version, threshold, QC criterion, or
analysis choice.

## Authority classes

| Class | Meaning | SOP label |
|---|---|---|
| Original protocol fact | Value explicitly supplied by the user's protocol or attachment. | Use as source, but still assess risk. |
| Local validated parameter | Value documented as validated in the user's lab/core/platform. | Executable if governance and QC are sufficient. |
| External benchmark | Value from peer-reviewed protocol, top-journal method, reporting standard, or benchmark paper. | Cite source; local validation status required. |
| Vendor/manual standard | Value from official kit, reagent, instrument, or software documentation. | Cite manual/version/access date. |
| Institutional/core-facility SOP | Value from a named local or institutional SOP. | Cite SOP/version/owner. |
| Recommended but unvalidated | Best-available value without local validation. | `★RECOMMENDED — TO BE VERIFIED LOCALLY`. |
| Unresolved gap | Value cannot be responsibly inferred. | `△TO BE CONFIRMED`. |
| Companion-derived lead | Tool/companion output that points to a source. | Not authoritative until source identity is resolved. |

## Hard rules

- Do not present recommended values as original protocol facts.
- Do not present vendor defaults as locally validated.
- Do not treat companion output as source authority unless resolved to a primary
  protocol, official manual, standard, repository record, or documented local SOP.
- Every recommended or substituted value must appear in the parameter provenance
  table with source identity and local verification status.
- Values affecting safety, animal welfare, sample fate, dose, incubation,
  centrifugation, sort gate, sequencing depth, library QC, statistical threshold,
  or exclusion rule require a readiness-contract entry.

## Parameter authority table

| Parameter | Protocol location | Proposed value | Authority class | Source identity | Local validation status | SOP label |
|---|---|---|---|---|---|---|
