from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_ROOT = ROOT / "benchmarks" / "v1.0"
SCORER = ROOT / "tools" / "score_protocol_benchmark.py"


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


if __name__ == "__main__":
    unittest.main()
