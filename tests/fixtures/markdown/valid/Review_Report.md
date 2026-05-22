# Review_Report.md

## 1. Protocol重建 / Protocol reconstruction

- Protocol: Demo flow cytometry staining SOP.
- Intended result: reproducible identification of a defined cell population.
- Primary readout: gated viable target-cell frequency.
- Experimental unit: one independently processed sample.
- Fragile step: antibody staining and compensation setup.

## 2. 执行摘要

The protocol is executable after adding explicit controls, QC gates, and source-linked parameter provenance.

## 3. 成熟度 / Readiness score

- Readiness score: 82/100.
- Maturity level: Level 2.
- Execution gate: executable with controls.

## 4. Module activation

| Module | Status | Reason |
| --- | --- | --- |
| flow_cytometry_and_imaging | active | Antibody staining, compensation, gating, and viability QC are required. |
| statistics_and_reproducibility | active | The experimental unit and batch record must be explicit. |

## 5. Evidence benchmark table

| Question | Source | Parameter or control | Local status |
| --- | --- | --- | --- |
| Is FMO control required? | MIFlowCyt, PMID:18752282 | FMO and single-stain controls | known_from_source |

## 6. Protocol Readiness Contract

| Field | Locked value |
| --- | --- |
| Intended result | Reproducible identification of a defined cell population. |
| Primary readout | Gated viable target-cell frequency. |
| Experimental unit | One independently processed sample. |
| Decisive QC gates | Viability gate, FMO threshold, compensation matrix. |
| Local validation requirements | Flow core confirms the fluorophore panel before execution. |

## 7. Parameter authority

| Parameter | Authority class | Source identity | Local validation status |
| --- | --- | --- | --- |
| FMO control | guideline_or_standard | MIFlowCyt, PMID:18752282 | Flow core confirms panel before execution. |

## 8. Readout contracts

| Readout | Supported conclusion | Acceptance criterion | Fail action |
| --- | --- | --- | --- |
| Viable target-cell frequency | Target-cell frequency is interpretable only after viability and FMO gates pass. | Viability percentage and FMO threshold are recorded for every sample. | Repeat preparation or exclude with deviation record. |

## 9. Protocol panel synthesis

| Panel role | Finding |
| --- | --- |
| Core-facility operator | The SOP needs viability release criteria and FMO-defined gates before batch execution. |

## 10. Severity-ranked findings

### Major issue M01

- 具体问题: The original workflow does not specify a viability gate or fail action.
- 证据: MIFlowCyt requires sufficient flow-cytometry method detail for interpretation, PMID:18752282.
- 影响: Dead-cell carryover can distort the target-cell frequency and make datasets non-comparable.
- Failure mode: non-specific antibody binding and autofluorescence are mistaken for signal.
- 解决: Add a viability dye gate, record the viable-cell percentage, and reject samples below the local acceptance threshold.
- 决定性 readout: The revised SOP passes when viable-cell percentage and FMO-defined threshold are recorded for every sample.
- SOP location: Revised_Protocol section 7.

## 11. QC and Metadata review

- QC gate: viable-cell percentage, FMO threshold, compensation matrix, acquisition event count.

## 12. Data records and repository gate

| Output | Raw data | Metadata | Repository |
| --- | --- | --- | --- |
| Flow cytometry FCS files | FCS files retained with acquisition metadata. | sample ID, antibody panel, compensation matrix, viability percentage. | Local institutional storage unless publication requires deposition. |

## 13. 统计 / Statistical review

The experimental unit is one independently processed sample. Technical repeats are not treated as biological replicates.

## 14. 安全 / Safety and governance review

The workflow is compatible with institutional biosafety review for non-infectious fixed samples.

## 15. Assumption ledger

| Assumption | Required confirmation |
| --- | --- |
| Instrument configuration supports the fluorophore panel. | Flow core manager confirms before execution. |

## 16. Parameter provenance

| Parameter | Value | Source and citation | Status |
| --- | --- | --- | --- |
| FMO control | one per critical marker | MIFlowCyt, PMID:18752282 | known_from_source |

## 17. Operator burden budget

| Added field | Burden | Justification |
| --- | --- | --- |
| Viability percentage | low | Prevents uninterpretable low-quality acquisitions. |

## 18. mini-pilot

Run one positive-control and one negative-control sample before processing the full batch.

## 19. Original-to-revised mapping

| Original gap | Revised SOP section |
| --- | --- |
| Missing viability gate | Section 7 quality control |

## 20. Red-line self-audit

No request asks for harmful biological-agent creation, oversight evasion, or concealment.
