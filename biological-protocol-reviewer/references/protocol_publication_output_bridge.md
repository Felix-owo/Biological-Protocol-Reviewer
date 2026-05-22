# Protocol Publication Output Bridge

Use only after protocol-readiness judgment and SOP rewrite are complete. This
bridge converts a validated SOP into publication-facing or submission-facing
text. It must not change readiness score, issue severity, or parameter authority.

## Allowed outputs

- Methods-section outline.
- Nature Protocols-inspired structure notes.
- Data Availability / Data Records Appendix draft with placeholders.
- Reporting checklist mapping.
- Figure/readout summary for methods figures.
- Author-facing Chinese clarification list.

## Rules

- Do not invent repository accessions, approvals, catalog numbers, RRIDs,
  software versions, dataset DOIs, licenses, or embargo dates.
- Keep executable SOP parameters tied to the SOP and parameter provenance table.
- If the publication-facing text needs a missing value, use
  `AUTHOR/LAB INPUT NEEDED` rather than filling it.
- Do not let style polishing hide missing execution parameters, QC gates, local
  validation, or safety/governance prerequisites.

## Methods handoff table

| SOP section | Publication-facing summary | Required citation/source | Missing author input |
|---|---|---|---|
