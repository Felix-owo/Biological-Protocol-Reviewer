# Protocol Readiness Contract

Use after reconstruction, evidence benchmarking, safety/governance review, and
failure-mode audit, but before rewriting executable SOP steps. The contract
prevents SOP prose from silently converting unknowns into executable facts.

## Required contract fields

| Field | Required content |
|---|---|
| intended_result | The biological or technical outcome the protocol must produce. |
| primary_readout | The readout that determines whether the protocol worked. |
| experimental_unit | Animal, sample, cell culture, library, image field, sort, sequencing run, or analysis unit. |
| decisive_QC_gates | QC gates that trigger release, rescue, repeat, exclusion, or stop. |
| local_validation_requirements | Controls, mini-pilot, acceptance thresholds, and repeat/rescue/exclude rules. |
| red_line_safety_governance_checks | Safety, ethics, biosafety, animal/human/material oversight checks. |
| parameters_not_to_fill | Values that must remain `△TO BE CONFIRMED` or `★RECOMMENDED — TO BE VERIFIED LOCALLY`. |
| maturity_gate_conditions | Conditions that keep the protocol at Level 0, 1, 2, or 3. |

## Lock rules

- Do not write an executable step for a missing dose, sequence, clone, RRID,
  centrifugation setting, incubation, threshold, sequencing depth, software
  version, or instrument setting unless the parameter authority is explicit.
- If a parameter is defensible but not locally validated, mark it
  `★RECOMMENDED — TO BE VERIFIED LOCALLY` and add mini-pilot validation when it
  can affect result interpretation.
- If no defensible value exists, mark it `△TO BE CONFIRMED` and state who or
  what must confirm it.
- SOP rewrite may improve clarity and structure but must not weaken readiness
  gates or hide unresolved gaps.
- A contract amendment after SOP rewrite must be logged in the review report
  with reason, source identity, and affected SOP section.
