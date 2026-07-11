# Runtime Profiles

Select one profile before loading domain resources. Profiles change context and
deliverables, never evidence, safety, traceability, or readiness standards.

## Reproducible resource budgets

Count only reference/template/schema files opened for the scientific task; do not
count the user artifact itself, generated output, or validator source. Character
counts are UTF-8 decoded text characters before chunking. The canonical limits
and baseline resource allowlists are machine-readable in
`references/skill_manifest.json`; package validation reads every allowlisted file
and fails if its file or character total exceeds the selected budget:

| Profile | Maximum reference files | Maximum reference characters |
| --- | ---: | ---: |
| `protocol_gate` | 10 | 80000 |
| `protocol_full` | 22 | 180000 |
| `delta_review` | 9 | 70000 |

If a budget would be exceeded, record the reason and move to the next justified
profile instead of silently expanding context. Repeated reads of the same file
count once. Tests and package validation must keep this table synchronized with
the manifest.

## `protocol_gate` (default)

Use for a first review or a PL-to-EXP decision. Load module routing, the rubric,
evidence/source gates, red-line rules, issue blocks, and only the routed domain
modules. Produce `Review_Report.md`. Do not rewrite the SOP. Panel synthesis,
operator-burden, mini-pilot, and review-to-SOP mapping sections are included only
when their applicability flag is true.

## `protocol_full`

Use only when the user explicitly requests an SOP rewrite or a complete
review-plus-SOP package. Complete `protocol_gate` first, then load operator
detailing, burden/mini-pilot, change-traceability, Markdown style, SOP template,
checklist, and output validator resources. Produce `Review_Report.md` and
`Revised_Protocol.md`. The full profile requires panel synthesis, operator-burden
budget, mini-pilot decision, and review-to-SOP mapping.

## `delta_review`

Use when a prior report exists and the user supplies changed protocol sections
or asks whether named blockers were resolved. Load the previous readiness
contract, open findings, changed sections, and only affected modules. Report
resolved, unchanged, new, and stale findings plus the updated gate. Do not
re-score untouched sections or rewrite the SOP unless explicitly requested.
The machine trace must include a prior review ID, changed artifact IDs, prior open
finding IDs, and the resolved, new, and carried-forward ID sets. Prior open IDs
must equal the disjoint union of resolved and carried-forward IDs; new IDs cannot
reuse prior IDs.

If the request is ambiguous, choose `protocol_gate`. Escalate from a smaller
profile only when the missing context could change the readiness decision.
