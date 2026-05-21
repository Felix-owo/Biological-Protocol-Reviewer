from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "Biological-Protocol-Reviewer" / "scripts" / "lint_structured_protocol.py"
SCHEMA_DIR = ROOT / "Biological-Protocol-Reviewer" / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "structured"


class SchemaLinterTests(unittest.TestCase):
    def test_all_schema_files_are_valid_json(self) -> None:
        for schema_path in SCHEMA_DIR.glob("*.schema.json"):
            with self.subTest(schema=schema_path.name):
                json.loads(schema_path.read_text(encoding="utf-8"))

    def test_valid_structured_report_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LINTER), str(FIXTURES / "valid_review_report.json")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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


if __name__ == "__main__":
    unittest.main()
