# Protocol Failure Mode Playbook

## Silent failure modes

- Reagent degradation without visible change.
- Incorrect final concentration due to ambiguous stock/working solution notation.
- Batch confounding with biological condition.
- Misidentified experimental unit.
- Cell-line drift, contamination, mycoplasma, or passage effects.
- Partial induction, mosaic recombination, or reporter leakiness.
- Antibody lot/clone failure or fluorophore mismatch.
- Library over-amplification, index hopping, low complexity, or carryover.
- Computational filtering that removes true biology or enriches artifacts.

## Red-line rewrite triggers

Rewrite the protocol if it contains:

- “As needed”, “appropriate amount”, “standard condition”, or “normal result”
  without numeric range or acceptance criteria.
- Control names without their artifact-detection role.
- QC steps without pass/fail action.
- Data analysis without the experimental unit.
- Omics analysis without metadata and deposition plan.
- Animal work without ethics scope, monitoring, and endpoint logic.

## Reviewer self-audit before final answer

Before returning, check:

- Did I identify the central conclusion protected by each control?
- Did I separate critical flaws from optional optimization?
- Did I avoid inventing unsupported operational values?
- Did I convert review comments into executable SOP edits?
- Did I explicitly name missing information that blocks interpretation?
