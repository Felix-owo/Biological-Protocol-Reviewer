from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "biological-protocol-reviewer"


class LicenseConsistencyTests(unittest.TestCase):
    def test_license_is_mpl2_across_primary_metadata(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

        self.assertIn("Mozilla Public License Version 2.0", license_text)
        self.assertIn("license: MPL-2.0", skill_text)
        self.assertIn('license = { text = "MPL-2.0" }', pyproject_text)


if __name__ == "__main__":
    unittest.main()
