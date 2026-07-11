from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "biological-protocol-reviewer"


class SkillPackageIntegrityTests(unittest.TestCase):
    def test_manifest_resource_paths_exist(self) -> None:
        manifest = json.loads((SKILL_ROOT / "references" / "skill_manifest.json").read_text(encoding="utf-8"))
        for rel_path in manifest.get("structured_format_resources", []):
            with self.subTest(path=rel_path):
                self.assertTrue((SKILL_ROOT / rel_path).exists(), rel_path)

    def test_default_profile_is_review_only(self) -> None:
        manifest = json.loads((SKILL_ROOT / "references" / "skill_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["runtime_profiles"]["default"], "protocol_gate")
        self.assertEqual(manifest["required_outputs"], ["Review_Report.md"])
        self.assertEqual(manifest["optional_outputs"], ["Revised_Protocol.md"])

    def test_runtime_profiles_have_reproducible_resource_budgets(self) -> None:
        manifest = json.loads((SKILL_ROOT / "references" / "skill_manifest.json").read_text(encoding="utf-8"))
        profiles = manifest["runtime_profiles"]
        profile_doc = (SKILL_ROOT / "references" / "runtime_profiles.md").read_text(encoding="utf-8")
        for profile in ["protocol_gate", "protocol_full", "delta_review"]:
            with self.subTest(profile=profile):
                budget = profiles[profile]
                self.assertGreater(budget["max_reference_files"], 0)
                self.assertGreater(budget["max_reference_characters"], 0)
                resources = budget["baseline_resources"]
                self.assertEqual(len(resources), len(set(resources)))
                self.assertLessEqual(len(resources), budget["max_reference_files"])
                character_count = sum(
                    len((SKILL_ROOT / resource).read_text(encoding="utf-8"))
                    for resource in resources
                )
                self.assertLessEqual(character_count, budget["max_reference_characters"])
                self.assertIn(
                    f"| `{profile}` | {budget['max_reference_files']} | {budget['max_reference_characters']} |",
                    profile_doc,
                )
        self.assertLessEqual(
            profiles["protocol_gate"]["max_reference_files"],
            profiles["protocol_full"]["max_reference_files"],
        )

    def test_skill_md_referenced_local_paths_exist(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        paths = sorted(set(re.findall(r"`((?:references|templates|scripts|schemas)/[^`]+)`", skill_text)))
        self.assertGreater(len(paths), 8)
        for rel_path in paths:
            if "*.schema.json" in rel_path:
                self.assertTrue((SKILL_ROOT / "schemas").exists())
                continue
            with self.subTest(path=rel_path):
                self.assertTrue((SKILL_ROOT / rel_path).exists(), rel_path)

    def test_installable_skill_checker_passes(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SKILL_ROOT / "scripts" / "check_installable_skill.py"),
                "--skill-dir",
                str(SKILL_ROOT),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_package_self_validates_when_cache_directory_is_renamed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cached_package = Path(tmpdir) / "opaque-cache-entry"
            shutil.copytree(SKILL_ROOT, cached_package)
            checker = cached_package / "scripts" / "check_installable_skill.py"
            result = subprocess.run(
                [sys.executable, str(checker), "--skill-dir", str(cached_package)],
                cwd=tmpdir,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_installable_checker_enforces_recursive_schema_dependency_closure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cached_package = Path(tmpdir) / "opaque-cache-entry"
            shutil.copytree(SKILL_ROOT, cached_package)
            (cached_package / "schemas" / "bioinformatics_handoff.schema.json").unlink()
            checker = cached_package / "scripts" / "check_installable_skill.py"
            result = subprocess.run(
                [sys.executable, str(checker), "--skill-dir", str(cached_package)],
                cwd=tmpdir,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bioinformatics_handoff.schema.json", result.stdout + result.stderr)

    def test_release_version_checker_keeps_repository_checks(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SKILL_ROOT / "scripts" / "check_version_consistency.py"),
                "--mode",
                "release",
                "--repo-root",
                str(ROOT),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
