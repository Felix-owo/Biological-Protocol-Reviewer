from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "biological-protocol-reviewer" / "scripts" / "protocol_output_validator.py"
VALID_MARKDOWN = ROOT / "tests" / "fixtures" / "markdown" / "valid"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("protocol_output_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def gate_report_text() -> str:
    text = (VALID_MARKDOWN / "Review_Report.md").read_text(encoding="utf-8")
    text = text.replace("**Runtime profile:** protocol_full", "**Runtime profile:** protocol_gate")
    full_only = (
        "Protocol panel synthesis",
        "Operator burden budget",
        "mini-pilot",
        "Original-to-revised mapping",
        "Review-to-SOP mapping",
    )
    for title in full_only:
        text = re.sub(
            rf"(?ms)^##\s+[^\n]*{re.escape(title)}[^\n]*\n.*?(?=^##\s+|\Z)",
            "",
            text,
        )
    return text


class ProtocolOutputValidatorTests(unittest.TestCase):
    def test_valid_markdown_fixture_passes(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--profile",
                "protocol_full",
                "--report",
                str(VALID_MARKDOWN / "Review_Report.md"),
                "--protocol",
                str(VALID_MARKDOWN / "Revised_Protocol.md"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_review_only_markdown_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report = Path(tmpdir) / "Review_Report.md"
            report.write_text(gate_report_text(), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    "--profile",
                    "protocol_gate",
                    "--report",
                    str(report),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_vague_language_is_detected(self) -> None:
        validator = load_validator_module()
        hits = validator.vague_hits("Add an appropriate amount of buffer before acquisition.")
        self.assertGreaterEqual(len(hits), 1)

    def test_recommended_parameter_requires_provenance(self) -> None:
        validator = load_validator_module()
        self.assertTrue(validator.recommended_without_provenance("★RECOMMENDED: use 1 ug input."))
        self.assertFalse(
            validator.recommended_without_provenance(
                "★RECOMMENDED: use 1 ug input. Parameter provenance: PMID:12345678."
            )
        )

    def test_readiness_score_and_level_must_be_consistent(self) -> None:
        validator = load_validator_module()
        self.assertTrue(validator.readiness_errors("Readiness score: 82/100\nMaturity level: Level 2"))
        self.assertTrue(validator.readiness_errors("Readiness score: 8.2/10\nMaturity level: Level 2"))
        self.assertTrue(validator.readiness_errors("Readiness score: 6-8/10\nMaturity level: Level 2"))
        self.assertTrue(validator.readiness_errors("Readiness score: 0.0-10.0\nMaturity level: Level 0 / 1 / 2 / 3"))
        self.assertTrue(validator.readiness_errors("Readiness score: <score>/10\nMaturity level: Level 2"))
        self.assertEqual(
            validator.readiness_errors("Readiness score: 7.2/10\nMaturity level: Level 2"),
            [],
        )

    def test_profile_is_required_and_must_match_report(self) -> None:
        missing = subprocess.run(
            [sys.executable, str(VALIDATOR), "--report", str(VALID_MARKDOWN / "Review_Report.md")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(missing.returncode, 0)
        mismatch = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--profile",
                "protocol_gate",
                "--report",
                str(VALID_MARKDOWN / "Review_Report.md"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(mismatch.returncode, 0)
        self.assertIn("does not match", mismatch.stdout)

    def test_operator_burden_rejects_medium(self) -> None:
        text = (VALID_MARKDOWN / "Review_Report.md").read_text(encoding="utf-8")
        text = text.replace("| Viability percentage | low |", "| Viability percentage | medium |")
        with tempfile.TemporaryDirectory() as tmpdir:
            report = Path(tmpdir) / "Review_Report.md"
            report.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    "--profile",
                    "protocol_full",
                    "--report",
                    str(report),
                    "--protocol",
                    str(VALID_MARKDOWN / "Revised_Protocol.md"),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("low, moderate, or high", result.stdout)

    def test_delta_review_requires_trace_and_enforces_id_partition(self) -> None:
        text = gate_report_text().replace(
            "**Runtime profile:** protocol_gate",
            "**Runtime profile:** delta_review",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            report = Path(tmpdir) / "Review_Report.md"
            report.write_text(text, encoding="utf-8")
            missing = subprocess.run(
                [sys.executable, str(VALIDATOR), "--profile", "delta_review", "--report", str(report)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(missing.returncode, 0)
            trace = """
- Prior review ID: PR-1
- Changed artifact IDs: step-4-v2
- Prior open finding IDs: M01, M02
- Resolved finding IDs: M01
- New finding IDs: M03
- Carried-forward finding IDs: M02
"""
            report.write_text(text.replace("**Runtime profile:** delta_review", "**Runtime profile:** delta_review\n" + trace), encoding="utf-8")
            valid = subprocess.run(
                [sys.executable, str(VALIDATOR), "--profile", "delta_review", "--report", str(report)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)

    def test_strict_content_is_default_and_lenient_is_explicit(self) -> None:
        text = gate_report_text() + "\n△TO BE CONFIRMED\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            report = Path(tmpdir) / "Review_Report.md"
            report.write_text(text, encoding="utf-8")
            command = [
                sys.executable,
                str(VALIDATOR),
                "--profile",
                "protocol_gate",
                "--report",
                str(report),
            ]
            strict = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
            lenient = subprocess.run(
                [*command, "--lenient-content", "--json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(strict.returncode, 0)
        self.assertIn("TO BE CONFIRMED", strict.stdout)
        self.assertEqual(lenient.returncode, 0, lenient.stdout + lenient.stderr)
        lenient_payload = json.loads(lenient.stdout)
        self.assertFalse(lenient_payload["decision_eligible"])
        self.assertTrue(any("not decision-eligible" in item for item in lenient_payload["warnings"]))


if __name__ == "__main__":
    unittest.main()
