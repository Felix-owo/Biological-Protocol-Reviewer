from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden"


class GoldenFixtureTests(unittest.TestCase):
    def test_golden_expected_contract_is_complete(self) -> None:
        expected = json.loads((GOLDEN / "protocol_missing_qc_expected.json").read_text(encoding="utf-8"))
        self.assertEqual(expected["case_id"], "golden_missing_flow_qc")
        self.assertGreaterEqual(len(expected["must_detect"]), 5)
        self.assertIn("minimum_severity", expected)
        self.assertIn("required_sop_sections", expected)
        self.assertTrue((GOLDEN / "protocol_missing_qc_input.md").exists())


if __name__ == "__main__":
    unittest.main()
