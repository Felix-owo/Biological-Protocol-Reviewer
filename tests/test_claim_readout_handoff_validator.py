from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "biological-protocol-reviewer" / "scripts" / "check_claim_readout_handoff.py"
FIXTURES = ROOT / "tests" / "fixtures" / "structured"
VALID = ROOT / "biological-protocol-reviewer" / "examples" / "regression_fixtures" / "handoff_figure_readout_missing_qc.json"


class ClaimReadoutHandoffValidatorTests(unittest.TestCase):
    def test_valid_handoff_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(VALID)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_empty_source_id_fails(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(FIXTURES / "invalid_claim_readout_empty_source_id.json")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source_ids[0]", result.stderr)


if __name__ == "__main__":
    unittest.main()
