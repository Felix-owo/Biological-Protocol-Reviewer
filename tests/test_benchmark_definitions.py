from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_ROOT = ROOT / "benchmarks" / "v1.0"
SCORER = ROOT / "tools" / "score_protocol_benchmark.py"
V150_SUMMARY = ROOT / "benchmarks" / "results" / "v1.5.0" / "benchmark_summary.json"


def load_scorer_module():
    spec = importlib.util.spec_from_file_location("score_protocol_benchmark", SCORER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ADVERSARIAL_SPEC = {
    "must_detect": ["FMO", "viability gate"],
    "minimum_severity": "Major",
    "forbidden_readiness_levels": ["Level 3"],
    "required_sop_sections": ["质量控制"],
}


def reasoned_output(score: str = "5.0/10", level: str = "Level 1") -> str:
    return f"""
Readiness score: {score}
Maturity level: {level}

### M1. Missing flow controls

**具体问题：** FMO and viability gate controls are absent from the protocol.
**证据：** The acquisition section names neither control nor an equivalent release record.
**影响：** Signal and dead-cell artefact cannot be distinguished reliably.
**解决：** Add the controls and record a release decision for every sample.
**决定性 readout：** A predefined pass threshold and repeat or exclusion action are recorded.

## 质量控制
"""


class BenchmarkDefinitionTests(unittest.TestCase):
    def test_benchmark_definitions_are_valid(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCORER), "--benchmark-root", str(BENCHMARK_ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_expected_findings_have_matching_case_files(self) -> None:
        expected = json.loads((BENCHMARK_ROOT / "expected_findings.json").read_text(encoding="utf-8"))
        for case_id in expected:
            with self.subTest(case_id=case_id):
                self.assertTrue((BENCHMARK_ROOT / "cases" / f"{case_id}.md").exists())

    def test_v150_pending_summary_does_not_claim_model_scores(self) -> None:
        summary = json.loads(V150_SUMMARY.read_text(encoding="utf-8"))
        self.assertEqual(summary["version"], "1.5.0")
        self.assertEqual(summary["status"], "pending_model_output_scoring")
        self.assertFalse(summary["model_outputs_scored"])
        self.assertIsNone(summary["mean_score"])
        self.assertIsNone(summary["pass_rate"])

    def test_keyword_stuffing_cannot_pass_behavioral_gate(self) -> None:
        scorer = load_scorer_module()
        output = """
Readiness score: 5.0/10
Maturity level: Level 1
Major FMO viability gate 质量控制
"""
        result = scorer.score_output(output, ADVERSARIAL_SPEC)
        self.assertEqual(result["must_detect_recall"], 0.0)
        self.assertFalse(result["behavioral_structure_ok"])
        self.assertFalse(result["pass"])

    def test_global_keyword_inventory_cannot_borrow_a_generic_reasoned_finding(self) -> None:
        scorer = load_scorer_module()
        output = """
Readiness score: 5.0/10
Maturity level: Level 1

### M1. Generic workflow concern
**具体问题：** The workflow has an unspecified quality concern unrelated to a named control.
**证据：** The methods omit a release record for the generic workflow concern.
**影响：** The result may not be interpretable without a completed quality record.
**解决：** Add a justified control and record its release decision before execution.
**决定性 readout：** A completed release record supports execution; failure blocks the run.

Keyword inventory: FMO; viability gate.
## 质量控制
"""
        result = scorer.score_output(output, ADVERSARIAL_SPEC)
        self.assertEqual(result["reasoned_finding_count"], 1)
        self.assertEqual(result["must_detect_recall"], 0.0)
        self.assertFalse(result["severity_ok"])
        self.assertFalse(result["pass"])

    def test_concept_must_link_to_a_finding_at_the_required_severity(self) -> None:
        scorer = load_scorer_module()
        output = reasoned_output().replace("### M1.", "### m1.")
        result = scorer.score_output(output, ADVERSARIAL_SPEC)
        self.assertEqual(result["reasoned_finding_count"], 1)
        self.assertEqual(result["must_detect_recall"], 0.0)
        self.assertFalse(result["severity_ok"])
        self.assertFalse(result["pass"])

    def test_wrong_readiness_scale_cannot_pass(self) -> None:
        scorer = load_scorer_module()
        result = scorer.score_output(reasoned_output(score="82/100"), ADVERSARIAL_SPEC)
        self.assertTrue(result["behavioral_structure_ok"])
        self.assertFalse(result["readiness_contract_ok"])
        self.assertFalse(result["pass"])

    def test_readiness_range_or_template_value_cannot_pass(self) -> None:
        scorer = load_scorer_module()
        for score, level in [
            ("6-8/10", "Level 2"),
            ("0.0-10.0", "Level 0 / 1 / 2 / 3"),
            ("<score>/10", "Level 2"),
        ]:
            with self.subTest(score=score, level=level):
                result = scorer.score_output(reasoned_output(score=score, level=level), ADVERSARIAL_SPEC)
                self.assertFalse(result["readiness_contract_ok"])
                self.assertFalse(result["pass"])

    def test_reasoned_finding_with_consistent_readiness_can_pass(self) -> None:
        scorer = load_scorer_module()
        result = scorer.score_output(reasoned_output(), ADVERSARIAL_SPEC)
        self.assertTrue(result["pass"], result)


if __name__ == "__main__":
    unittest.main()
