from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "biological-protocol-reviewer" / "scripts" / "lint_structured_protocol.py"
SCHEMA_DIR = ROOT / "biological-protocol-reviewer" / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "structured"
VALID_HANDOFF = (
    ROOT
    / "biological-protocol-reviewer"
    / "examples"
    / "regression_fixtures"
    / "handoff_figure_readout_missing_qc.json"
)


def load_linter_module():
    spec = importlib.util.spec_from_file_location("lint_structured_protocol", LINTER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SchemaLinterTests(unittest.TestCase):
    def test_all_schema_files_are_valid_json(self) -> None:
        for schema_path in SCHEMA_DIR.glob("*.schema.json"):
            with self.subTest(schema=schema_path.name):
                json.loads(schema_path.read_text(encoding="utf-8"))


    def test_valid_external_companion_evidence_passes(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(LINTER),
                str(FIXTURES / "valid_external_companion_evidence.json"),
                "--schema",
                str(SCHEMA_DIR / "external_companion_evidence.schema.json"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_external_companion_requires_primary_source(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(LINTER),
                str(FIXTURES / "invalid_external_companion_missing_source.json"),
                "--schema",
                str(SCHEMA_DIR / "external_companion_evidence.schema.json"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("primary_source_resolved", result.stderr)

    def test_valid_structured_report_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LINTER), str(FIXTURES / "valid_review_report.json")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_readiness_score_uses_zero_to_ten_number_contract(self) -> None:
        linter = load_linter_module()
        schema = json.loads((SCHEMA_DIR / "review_report.schema.json").read_text(encoding="utf-8"))
        fixture = json.loads((FIXTURES / "valid_review_report.json").read_text(encoding="utf-8"))

        for boundary, maturity in ((0, 0), (10, 3), (7.25, 2)):
            with self.subTest(score=boundary, maturity=maturity):
                report = copy.deepcopy(fixture)
                report["readiness"]["score"] = boundary
                report["readiness"]["maturity_level"] = maturity
                self.assertEqual(linter.validate_output(report, schema), [])

        for invalid in (-0.1, 10.1, 82):
            with self.subTest(score=invalid):
                report = copy.deepcopy(fixture)
                report["readiness"]["score"] = invalid
                errors = linter.validate_output(report, schema)
                self.assertTrue(any("score" in error for error in errors), errors)

    def test_readiness_score_must_match_maturity_level(self) -> None:
        linter = load_linter_module()
        schema = json.loads((SCHEMA_DIR / "review_report.schema.json").read_text(encoding="utf-8"))
        fixture = json.loads((FIXTURES / "valid_review_report.json").read_text(encoding="utf-8"))
        fixture["readiness"]["score"] = 8.2
        fixture["readiness"]["maturity_level"] = 2
        errors = linter.validate_output(fixture, schema)
        self.assertTrue(any("inconsistent with maturity_level" in error for error in errors), errors)

    def test_operator_burden_uses_low_moderate_high(self) -> None:
        linter = load_linter_module()
        schema = json.loads((SCHEMA_DIR / "review_report.schema.json").read_text(encoding="utf-8"))
        fixture = json.loads((FIXTURES / "valid_review_report.json").read_text(encoding="utf-8"))

        fixture["operator_burden_budget"][0]["burden"] = "moderate"
        self.assertEqual(linter.validate_schema(fixture, schema), [])
        fixture["operator_burden_budget"][0]["burden"] = "medium"
        errors = linter.validate_schema(fixture, schema)
        self.assertTrue(any("burden" in error for error in errors), errors)

    def test_valid_structured_protocol_passes(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(LINTER),
                str(FIXTURES / "valid_revised_protocol.json"),
                "--schema",
                str(SCHEMA_DIR / "revised_protocol.schema.json"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_valid_claim_handoff_supports_local_schema_defs(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(LINTER),
                str(VALID_HANDOFF),
                "--schema",
                str(SCHEMA_DIR / "claim_readout_handoff.schema.json"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_claim_handoff_schema_rejects_version_and_duplicate_source_ids(self) -> None:
        for fixture_name, expected in [
            ("invalid_claim_readout_version.json", "must equal '1.0.0'"),
            ("invalid_claim_readout_duplicate_source.json", "array items must be unique"),
        ]:
            with self.subTest(fixture=fixture_name):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(LINTER),
                        str(FIXTURES / fixture_name),
                        "--schema",
                        str(SCHEMA_DIR / "claim_readout_handoff.schema.json"),
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)

    def test_missing_issue_decisive_readout_fails(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LINTER), str(FIXTURES / "invalid_issue_missing_readout.json")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("decisive_readout", result.stderr)

    def test_protocol_gate_does_not_require_full_only_sections(self) -> None:
        linter = load_linter_module()
        schema = json.loads((SCHEMA_DIR / "review_report.schema.json").read_text(encoding="utf-8"))
        report = json.loads((FIXTURES / "valid_review_report.json").read_text(encoding="utf-8"))
        report["runtime_profile"] = "protocol_gate"
        report["profile_contract"] = {
            "protocol_panel_applicable": False,
            "operator_burden_applicable": False,
            "mini_pilot_applicable": False,
            "review_to_sop_mapping_applicable": False,
        }
        for field in [
            "protocol_panel_synthesis",
            "operator_burden_budget",
            "mini_pilot_plan",
            "review_to_sop_mapping",
        ]:
            report.pop(field)
        self.assertEqual(linter.validate_output(report, schema), [])

    def test_protocol_full_requires_full_profile_sections(self) -> None:
        linter = load_linter_module()
        schema = json.loads((SCHEMA_DIR / "review_report.schema.json").read_text(encoding="utf-8"))
        report = json.loads((FIXTURES / "valid_review_report.json").read_text(encoding="utf-8"))
        report.pop("operator_burden_budget")
        errors = linter.validate_output(report, schema)
        self.assertTrue(any("operator_burden_budget" in error for error in errors), errors)

    def test_applicability_flag_requires_corresponding_section(self) -> None:
        linter = load_linter_module()
        schema = json.loads((SCHEMA_DIR / "review_report.schema.json").read_text(encoding="utf-8"))
        report = json.loads((FIXTURES / "valid_review_report.json").read_text(encoding="utf-8"))
        report["runtime_profile"] = "protocol_gate"
        report["profile_contract"]["mini_pilot_applicable"] = True
        report.pop("mini_pilot_plan")
        errors = linter.validate_output(report, schema)
        self.assertTrue(any("mini_pilot_plan" in error for error in errors), errors)

    def test_delta_review_requires_complete_consistent_trace(self) -> None:
        linter = load_linter_module()
        schema = json.loads((SCHEMA_DIR / "review_report.schema.json").read_text(encoding="utf-8"))
        report = json.loads((FIXTURES / "valid_review_report.json").read_text(encoding="utf-8"))
        report["runtime_profile"] = "delta_review"
        report["profile_contract"] = {
            "protocol_panel_applicable": False,
            "operator_burden_applicable": False,
            "mini_pilot_applicable": False,
            "review_to_sop_mapping_applicable": False,
        }
        for field in [
            "protocol_panel_synthesis",
            "operator_burden_budget",
            "mini_pilot_plan",
            "review_to_sop_mapping",
        ]:
            report.pop(field)
        missing_errors = linter.validate_output(report, schema)
        self.assertTrue(any("delta_review_trace" in error for error in missing_errors), missing_errors)

        report["delta_review_trace"] = {
            "prior_review_id": "PR-1",
            "changed_artifact_ids": ["step-4-v2"],
            "prior_open_finding_ids": ["M01", "M02"],
            "resolved_finding_ids": ["M01"],
            "new_finding_ids": ["M03"],
            "carried_forward_finding_ids": ["M02"],
        }
        self.assertEqual(linter.validate_output(report, schema), [])
        report["delta_review_trace"]["carried_forward_finding_ids"] = []
        errors = linter.validate_output(report, schema)
        self.assertTrue(any("prior_open_finding_ids must equal" in error for error in errors), errors)

        report["delta_review_trace"]["prior_open_finding_ids"] = [{"bad": "id"}]
        errors = linter.validate_output(report, schema)
        self.assertTrue(any("prior_open_finding_ids" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
