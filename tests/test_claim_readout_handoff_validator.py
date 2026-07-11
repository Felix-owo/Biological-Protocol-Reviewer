from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "biological-protocol-reviewer" / "scripts" / "check_claim_readout_handoff.py"
FIXTURES = ROOT / "tests" / "fixtures" / "structured"
VALID = ROOT / "biological-protocol-reviewer" / "examples" / "regression_fixtures" / "handoff_figure_readout_missing_qc.json"


class ClaimReadoutHandoffValidatorTests(unittest.TestCase):
    def run_checker(self, artifact: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(artifact)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_handoff_passes(self) -> None:
        result = self.run_checker(VALID)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_empty_source_id_fails(self) -> None:
        result = self.run_checker(FIXTURES / "invalid_claim_readout_empty_source_id.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source_ids[0]", result.stderr)

    def test_extra_root_item_and_extension_fields_fail(self) -> None:
        result = self.run_checker(FIXTURES / "invalid_claim_readout_extra_field.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("root contains unsupported field `unexpected_root`", result.stderr)
        self.assertIn("contains unsupported field `unexpected_item`", result.stderr)
        self.assertIn("extensions contains unsupported field `unregistered_reviewer`", result.stderr)

    def test_wrong_contract_version_fails(self) -> None:
        result = self.run_checker(FIXTURES / "invalid_claim_readout_version.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("contract_version must be '1.0.0'", result.stderr)

    def test_duplicate_source_ids_fail(self) -> None:
        result = self.run_checker(FIXTURES / "invalid_claim_readout_duplicate_source.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicates source ID 'S1'", result.stderr)

    def test_protocol_step_or_method_uses_schema_minimum_length_four(self) -> None:
        artifact = json.loads(VALID.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "handoff.json"
            artifact["claim_readout_map"][0]["protocol_step_or_method"] = "step"
            path.write_text(json.dumps(artifact), encoding="utf-8")
            valid = self.run_checker(path)
            artifact["claim_readout_map"][0]["protocol_step_or_method"] = "abc"
            path.write_text(json.dumps(artifact), encoding="utf-8")
            invalid = self.run_checker(path)
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("protocol_step_or_method must be substantive", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
