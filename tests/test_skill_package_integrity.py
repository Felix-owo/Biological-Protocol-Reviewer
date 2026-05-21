from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "Biological-Protocol-Reviewer"


class SkillPackageIntegrityTests(unittest.TestCase):
    def test_manifest_resource_paths_exist(self) -> None:
        manifest = json.loads((SKILL_ROOT / "skill_manifest.json").read_text(encoding="utf-8"))
        for rel_path in manifest.get("structured_format_resources", []):
            with self.subTest(path=rel_path):
                self.assertTrue((SKILL_ROOT / rel_path).exists(), rel_path)

    def test_skill_md_referenced_local_paths_exist(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        paths = sorted(set(re.findall(r"`((?:references|templates|validators|scripts|schemas)/[^`]+)`", skill_text)))
        self.assertGreater(len(paths), 8)
        for rel_path in paths:
            if "*.schema.json" in rel_path:
                self.assertTrue((SKILL_ROOT / "schemas").exists())
                continue
            with self.subTest(path=rel_path):
                self.assertTrue((SKILL_ROOT / rel_path).exists(), rel_path)


if __name__ == "__main__":
    unittest.main()
