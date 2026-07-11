from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "biological-protocol-reviewer" / "scripts" / "check_protocol_passport.py"
FIXTURES = ROOT / "tests" / "fixtures" / "structured"
TEMPLATE = ROOT / "biological-protocol-reviewer" / "templates" / "protocol_passport_template.yaml"


class ProtocolPassportValidatorTests(unittest.TestCase):
    def run_checker(self, *args: str, no_site: bool = False) -> subprocess.CompletedProcess[str]:
        command = [sys.executable]
        if no_site:
            command.append("-S")
        command.extend([str(CHECKER), *args])
        return subprocess.run(
            command,
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

    def test_completed_yaml_fails_closed_without_pyyaml(self) -> None:
        strict = self.run_checker(str(TEMPLATE), no_site=True)
        self.assertNotEqual(strict.returncode, 0)
        self.assertIn("PyYAML is required", strict.stderr)

    def test_template_mode_has_limited_fallback_without_pyyaml(self) -> None:
        result = self.run_checker(str(TEMPLATE), "--allow-template", no_site=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("template identity was verified", result.stdout)

    def test_template_mode_rejects_modified_yaml_without_pyyaml(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8").replace('protocol_id: ""', 'protocol_id: "completed"', 1)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "modified-template.yaml"
            path.write_text(text, encoding="utf-8")
            result = self.run_checker(str(path), "--allow-template", no_site=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly matching the bundled", result.stderr)

    def test_checker_enforces_schema_minimum_lengths(self) -> None:
        text = (FIXTURES / "passport_valid_minimal.json").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "short.json"
            path.write_text(text.replace('"primary_readout": "fluorescence lineage readout"', '"primary_readout": "abc"'), encoding="utf-8")
            result = self.run_checker(str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("primary_readout must contain at least 4 characters", result.stderr)


if __name__ == "__main__":
    unittest.main()
