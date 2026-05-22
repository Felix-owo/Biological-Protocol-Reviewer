# Protocol Passport

Use for long protocols, resumed sessions, regression fixtures, structured audit
extracts, or when the user asks for an auditable state object. The passport is
not a third default user-facing deliverable; it is an optional state record that
supports `Review_Report.md` and `Revised_Protocol.md`.

## Passport fields

| Field | Purpose |
|---|---|
| protocol_id | Stable protocol identifier. |
| skill_version | Skill version used for review. |
| source_materials | User-supplied corpus and external sources screened. |
| sample_material | Organism, cell type, sample, tissue, library, or data object. |
| primary_readout | Readout that determines protocol success. |
| experimental_unit | Unit for interpretation and statistics. |
| module_activation | Activated modules and unclear modules. |
| resource_identity | Reagents, antibodies, primers, equipment, software, and missing IDs. |
| parameter_authority | Parameter classes and local validation status. |
| qc_gates | QC gates, thresholds, fail actions, and readout links. |
| local_validation_status | Validated, recommended-unvalidated, unresolved, or blocked. |
| safety_governance_status | Approval/training/facility status and red-line outcome. |
| unresolved_gaps | Items that block execution or interpretation. |
| mini_pilot_plan | Required local validation package. |
| review_to_sop_mapping | Finding-to-SOP revision trace. |
| validator_status | Markdown and structured validation results. |

## Rules

- Passport values must be traceable to the review report, revised SOP, or source
  table.
- Do not store secrets, credentials, private paths that should not be shared, or
  broad raw contents.
- If a field is unknown, use `unresolved` with a confirmation owner rather than
  inventing a value.
- When saving YAML, follow `templates/protocol_passport_template.yaml`; when
  saving JSON, validate against `schemas/protocol_passport.schema.json`.
