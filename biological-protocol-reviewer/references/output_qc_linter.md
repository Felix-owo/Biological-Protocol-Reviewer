# Output QC Linter

Run this check before final delivery.

When files exist, also run:

```bash
python3 scripts/protocol_output_validator.py --report Review_Report.md --protocol Revised_Protocol.md
```

Treat validator failure as a blocking issue unless the failure is a known false positive and the reason is documented in the final response.

## Required files

- `Review_Report.md` exists.
- `Revised_Protocol.md` exists.

## Review_Report.md checks

The report must contain:
- protocol identity, protocol reconstruction, and executive verdict;
- readiness score and Level 0-3 maturity gate;
- module activation table;
- evidence benchmark table;
- exact source identity for Grade A-C sources, including DOI/PMID/official URL/manual or standard version and access date when applicable;
- Critical/Major/Minor/Optimization sections;
- controls and QC gaps;
- metadata and data-record gaps;
- statistics and reproducibility review;
- safety, ethics, and biosafety review;
- assumption ledger when missing details are filled;
- parameter provenance table when recommended parameters are introduced;
- operator burden budget;
- mini-pilot plan when new, substituted, scaled, transferred, or locally unvalidated parameters are used;
- original-to-revised mapping table;
- required changes before execution;
- red-line self-audit.

Every Critical or Major issue must include:
- `具体问题`;
- `为什么严重` or `为什么重要`;
- `证据`, including original location plus internal and external evidence;
- `影响`, naming the threatened readout, conclusion, sample usability, safety, or auditability;
- `替代解释/漏洞`;
- `解决`;
- `决定性 readout`, including minimum criterion and stop/go rule;
- `SOP修订位置`.

## Revised_Protocol.md checks

The Markdown SOP must contain:
- SOP-first Nature Protocols-inspired section structure;
- document control near the top of the Markdown SOP;
- bench-facing execution summary before long background or governance prose;
- `Before you begin`, numbered procedure, reagent setup, and resources/equipment/primers/oligos/antibodies sections before appendices;
- numbered procedure with concrete parameters;
- purchase-ready reagent, consumable, equipment, primer/oligo, antibody/probe, and software tables;
- callout markers where relevant;
- QC release criteria;
- troubleshooting table;
- timing and pause points;
- anticipated results;
- reporting checklist in Appendix K unless the user requested otherwise;
- appendices A-K retained or marked Not applicable with reason;
- parameter provenance table if any `★RECOMMENDED` values are used;
- assumption ledger if unresolved context materially affects execution.
- mini-pilot plan when new, substituted, scaled, transferred, or locally unvalidated parameters are used;
- FAIR/data-quality release gates when the protocol produces omics, imaging, flow, or computationally interpreted outputs;
- Markdown structure from `references/markdown_sop_style.md` unless another user-specified structure overrides it.

The procedure section must not be buried behind long introduction, governance, design rationale, or reporting checklist sections. The first executable step must appear before long rationale or audit appendices unless the source protocol is unusually complex and the reason is stated.

## Vague-language blocklist

The final revised protocol must not leave the following unresolved unless immediately followed by a concrete parameter, validation plan, or `△TO BE CONFIRMED`:
- appropriate amount
- as needed
- standard protocol
- standard conditions
- follow kit instructions
- optimize if necessary
- sufficient volume
- suitable concentration
- room temperature without range or record requirement
- briefly
- carefully without specifying action

## Failure rule

If the linter fails, fix the deliverables before giving them to the user. If a tool limitation prevents fixing the issue, state the exact limitation in the final chat summary.
