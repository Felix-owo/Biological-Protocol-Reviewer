# Risk Classification and Red-line Rules

## Default scope

Assume legitimate institutional research only when the user-supplied context is consistent with trained personnel, appropriate facility, ordinary biological research aims, and compliant oversight. Missing approval identifiers are documentation gaps, not automatic refusal triggers.

## Documentation-gap handling

For ordinary regulated research, continue the review and rewrite but insert:
- approval ID placeholders
- personnel qualification records
- facility and room authorization records
- PPE and waste records
- deviation and incident logs
- `TO BE COMPLETED BEFORE EXECUTION` labels

## Dynamic governance and biosafety standard check

For recombinant or synthetic nucleic acids, viral vectors, human-derived material, pathogens, toxins, animal work, or regulated facilities, check the current official standard or landing page when web access is available. At minimum, consider NIH Guidelines for recombinant or synthetic nucleic acid molecules, CDC/NIH BMBL, WHO Laboratory Biosafety Manual, and local institutional requirements. Record the version or access date in the evidence/source table.

If current standards cannot be checked, do not invent a version. Mark the governance standard as `TO BE VERIFIED BEFORE EXECUTION`.

## Red-line topics

Do not provide operational protocol details when the request asks to:
- evade, bypass, or falsify institutional oversight;
- conceal adverse events, animal welfare events, contamination, exposure, or protocol deviations;
- execute regulated biological work outside a legitimate laboratory or approved facility;
- create, enhance, weaponize, disseminate, or optimize dangerous biological agents for harmful use;
- increase pathogenicity, transmissibility, host range, immune evasion, environmental persistence, or delivery of harmful agents;
- misuse toxins, controlled agents, or hazardous biological materials outside authorized governance.

## Degraded-output mode

If a request crosses a red line, provide only:
- governance and safety concerns;
- non-operational compliance checklist;
- recommendation to consult institutional biosafety/ethics/safety officers;
- high-level non-actionable conceptual alternatives.

## Severity integration

In `Review_Report.md`, classify red-line or governance-blocking defects as Critical. Administrative gaps that are routine and fixable are Major or Minor depending on their impact on execution, auditability, or interpretability.
