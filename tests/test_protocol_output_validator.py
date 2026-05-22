from __future__ import annotations

import importlib.util
import subprocess
import sys
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


class ProtocolOutputValidatorTests(unittest.TestCase):
    def test_valid_markdown_fixture_passes(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
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


if __name__ == "__main__":
    unittest.main()
