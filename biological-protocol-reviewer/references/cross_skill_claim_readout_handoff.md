# Cross-Skill Claim-Readout Handoff

Use when a protocol, SOP, method appendix, or data workflow is being reviewed in
the context of a manuscript, proposal, figure set, dataset, or central scientific
claim. This is the shared interface between Biological Protocol Reviewer and
Rigorous Reviewer.

## Purpose

Map protocol readouts and execution gates to the scientific claims they can
actually support. The handoff prevents SOP optimization from drifting away from
the manuscript claim, and prevents manuscript review from accepting a protocol
readout without checking parameter authority, QC gates, and failure modes.

## Required mapping

| Field | Required content |
|---|---|
| claim_id | Stable ID for the manuscript/proposal claim. |
| claim_text | Exact claim or conclusion under review. |
| evidence_role | decisive / supporting / contextual / exploratory. |
| readout_id | Stable protocol readout ID. |
| readout_supports | What the readout can support if it passes. |
| protocol_step_or_method | SOP section, method, assay, proof-of-measurement, or analysis step. |
| parameter_authority | original / local validated / external benchmark / recommended-unvalidated / unresolved. |
| qc_gate | QC threshold, positive/negative control, fail action, and record field. |
| failure_mode | False-positive, false-negative, safety, reproducibility, or interpretability risk. |
| manuscript_impact | How the claim changes if the readout or protocol gate fails. |
| revision_action | Add control / add validation / narrow claim / mark preliminary / author input needed. |
| source_ids | Evidence-ledger or source-table IDs supporting the mapping. |

## Rules

- A protocol readout cannot be treated as decisive unless it maps to a specific
  claim and includes a control, acceptance criterion, fail action, and
  interpretation boundary.
- If a decisive claim depends on `recommended-unvalidated` or `unresolved`
  parameters, the revised SOP must add mini-pilot validation or keep the claim
  handoff as blocked.
- If the protocol is strong but the manuscript claim overreaches the readout,
  mark the manuscript impact as `claim_narrowing_required`.
- If used in an SOP, record the mapping in readout contracts, parameter
  provenance, and review-to-SOP mapping. If used in a review, record it in the
  evidence ledger.
- Use `schemas/claim_readout_handoff.schema.json` and
  `scripts/check_claim_readout_handoff.py` when saving a machine-readable
  handoff artifact.
