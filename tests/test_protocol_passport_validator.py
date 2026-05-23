from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "biological-protocol-reviewer" / "scripts" / "check_protocol_passport.py"
FIXTURES = ROOT / "tests" / "fixtures" / "structured"
TEMPLATE = ROOT / "biological-protocol-reviewer" / "templates" / "protocol_passport_template.yaml"


class ProtocolPassportValidatorTests(unittest.TestCase):
    def run_checker(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_minimal_passport_passes(self) -> None:
        result = self.run_checker(str(FIXTURES / "passport_valid_minimal.json"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_qc_gates_fail(self) -> None:
        result = self.run_checker(str(FIXTURES / "passport_invalid_missing_qc.json"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("qc_gates", result.stderr)

    def test_blank_template_passes_only_in_template_mode(self) -> None:
        strict = self.run_checker(str(TEMPLATE))
        self.assertNotEqual(strict.returncode, 0)
        template_mode = self.run_checker(str(TEMPLATE), "--allow-template")
        self.assertEqual(template_mode.returncode, 0, template_mode.stdout + template_mode.stderr)


if __name__ == "__main__":
    unittest.main()
