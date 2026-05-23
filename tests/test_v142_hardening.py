from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "biological-protocol-reviewer"


class V142HardeningTests(unittest.TestCase):
    def test_manifest_resources_exist(self) -> None:
        manifest = json.loads((SKILL_ROOT / "references" / "skill_manifest.json").read_text(encoding="utf-8"))
        for resource in manifest.get("structured_format_resources", []):
            self.assertTrue((SKILL_ROOT / resource).exists(), resource)

    def test_external_companion_schema_has_auditable_identity_fields(self) -> None:
        schema = json.loads((SKILL_ROOT / "schemas" / "external_companion_evidence.schema.json").read_text(encoding="utf-8"))
        for field in ["identifier_type", "identifier", "resolved_source_grade"]:
            self.assertIn(field, schema["required"])
            self.assertIn(field, schema["properties"])
        self.assertIn("pattern", schema["properties"]["access_date"])

    def test_protocol_passport_schema_requires_nested_audit_fields(self) -> None:
        schema = json.loads((SKILL_ROOT / "schemas" / "protocol_passport.schema.json").read_text(encoding="utf-8"))
        self.assertIn("required", schema["properties"]["source_materials"])
        self.assertIn("required", schema["properties"]["sample_material"])
        self.assertIn("required", schema["properties"]["safety_governance_status"])
        self.assertIn("required", schema["properties"]["validator_status"])


if __name__ == "__main__":
    unittest.main()
