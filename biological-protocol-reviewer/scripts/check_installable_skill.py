#!/usr/bin/env python3
"""Smoke-test the installable biological-protocol-reviewer skill folder.

This validator checks the static package shape and cross-checks resource
references across SKILL.md, references/skill_manifest.json, and the filesystem.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

CANONICAL_NAME = "biological-protocol-reviewer"
REQUIRED_DIRS = ["agents", "examples", "references", "schemas", "scripts", "templates"]
ALLOWED_TOP_LEVEL = {"SKILL.md", *REQUIRED_DIRS}
BASE_REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/agent_behavior_core.md",
    "references/module_activation_and_routing.md",
    "references/evidence_benchmarking_workflow.md",
    "references/evidence_and_standards_hard_gates.md",
    "references/risk_classification_and_redlines.md",
    "references/protocol_rubric.json",
    "references/output_qc_linter.md",
    "references/sop_traceability_and_change_discipline.md",
    "references/revised_protocol_qc_checklist.md",
    "references/skill_manifest.json",
    "templates/Review_Report_template.md",
    "templates/Revised_Protocol_md_structure.md",
    "templates/issue_block_templates.json",
    "templates/source_search_hints.json",
    "schemas/review_report.schema.json",
    "schemas/revised_protocol.schema.json",
    "schemas/issue.schema.json",
    "schemas/qc_gate.schema.json",
    "schemas/parameter_provenance.schema.json",
    "schemas/bioinformatics_handoff.schema.json",
    "schemas/external_companion_evidence.schema.json",
    "schemas/protocol_passport.schema.json",
    "schemas/claim_readout_handoff.schema.json",
    "scripts/protocol_output_validator.py",
    "scripts/lint_structured_protocol.py",
    "scripts/check_installable_skill.py",
    "scripts/check_version_consistency.py",
    "scripts/run_regression_fixtures.py",
    "scripts/check_protocol_passport.py",
    "scripts/check_claim_readout_handoff.py",
]
DESCRIPTION_TERMS = ["protocol", "SOP", "QC", "benchmark", "readiness"]
ALLOWED_LICENSES = {"MPL-2.0"}
RESOURCE_PATTERN = re.compile(
    r"(?P<path>(?:agents|examples|references|schemas|scripts|templates)/[A-Za-z0-9_./-]+)"
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'")
    close_idx = text.find("\n---\n", 4)
    if close_idx == -1:
        raise ValueError("SKILL.md frontmatter must be closed by a second '---' delimiter")
    header = text[4:close_idx]
    data: dict[str, str] = {}
    for line in header.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line.strip())
        if match:
            key, value = match.groups()
            data[key] = value.strip().strip('"\'')
    desc_match = re.search(
        r"^description:\s*[>|]?\s*\n(?P<body>(?:^[ \t]+.*\n?)+)",
        header,
        flags=re.MULTILINE,
    )
    if desc_match:
        data["description"] = re.sub(r"\s+", " ", desc_match.group("body")).strip()
    return data, header


def extract_version_from_skill(text: str) -> str | None:
    match = re.search(r"metadata:\s*(?:\n\s+[A-Za-z0-9_-]+:.*)*\n\s+version:\s*\"([^\"]+)\"", text)
    if match:
        return match.group(1)
    match = re.search(r"^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, flags=re.MULTILINE)
    return match.group(1) if match else None


def load_manifest(skill_dir: Path, errors: list[str]) -> dict[str, object]:
    manifest_path = skill_dir / "references" / "skill_manifest.json"
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"Could not parse references/skill_manifest.json: {exc}")
        return {}


def referenced_resources_from_skill(text: str) -> set[str]:
    resources: set[str] = set()
    for match in RESOURCE_PATTERN.finditer(text):
        raw = match.group("path").rstrip("`),.;:")
        if "*" in raw:
            continue
        resources.add(raw)
    return resources


def manifest_resources(manifest: dict[str, object]) -> set[str]:
    resources: set[str] = set()
    for key in ["structured_format_resources"]:
        values = manifest.get(key, [])
        if isinstance(values, list):
            resources.update(item for item in values if isinstance(item, str))
    return resources


def schema_reference_errors(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    schema_root = skill_dir / "schemas"

    def references(value: object):
        if isinstance(value, dict):
            reference = value.get("$ref")
            if isinstance(reference, str):
                yield reference
            for nested in value.values():
                yield from references(nested)
        elif isinstance(value, list):
            for nested in value:
                yield from references(nested)

    for schema_path in sorted(schema_root.glob("*.json")):
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            errors.append(f"Invalid schema {schema_path.relative_to(skill_dir)}: {error}")
            continue
        for reference in references(schema):
            target_text = reference.split("#", 1)[0]
            if not target_text or "://" in target_text or target_text.startswith("urn:"):
                continue
            target = schema_path.parent / target_text
            if not target.is_file() or target.is_symlink():
                errors.append(
                    f"Schema dependency missing for {schema_path.relative_to(skill_dir)}: {target_text}"
                )
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    if not skill_dir.exists():
        return [f"Skill directory does not exist: {skill_dir}"]

    top_level = {path.name for path in skill_dir.iterdir()}
    unexpected = sorted(top_level - ALLOWED_TOP_LEVEL)
    if unexpected:
        errors.append(f"Unexpected top-level files/directories: {unexpected}")

    for dirname in REQUIRED_DIRS:
        if not (skill_dir / dirname).is_dir():
            errors.append(f"Missing required directory: {dirname}")
    for filename in BASE_REQUIRED_FILES:
        if not (skill_dir / filename).is_file():
            errors.append(f"Missing required file: {filename}")
    errors.extend(schema_reference_errors(skill_dir))
    if (skill_dir / "validators").exists():
        errors.append("Do not keep a top-level validators/ directory; use references/ or scripts/")

    skill_md = skill_dir / "SKILL.md"
    skill_text = ""
    skill_version = None
    if skill_md.exists():
        skill_text = skill_md.read_text(encoding="utf-8")
        skill_version = extract_version_from_skill(skill_text)
        try:
            meta, _ = parse_frontmatter(skill_text)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if meta.get("name") != CANONICAL_NAME:
                errors.append(f"SKILL.md frontmatter name must be {CANONICAL_NAME!r}")
            description = meta.get("description", "")
            if len(description) < 80:
                errors.append("SKILL.md description is too short for reliable trigger routing")
            missing_terms = [term for term in DESCRIPTION_TERMS if term.lower() not in description.lower()]
            if missing_terms:
                errors.append(f"SKILL.md description lacks trigger terms: {missing_terms}")
            license_value = meta.get("license", "")
            if license_value not in ALLOWED_LICENSES:
                errors.append(f"SKILL.md frontmatter license must be one of {sorted(ALLOWED_LICENSES)!r}")

        if "validators/revised_protocol_qc_checklist.md" in skill_text:
            errors.append("SKILL.md still references non-standard validators/ path")
        if "references/revised_protocol_qc_checklist.md" not in skill_text:
            errors.append("SKILL.md must route the revised-protocol QC checklist from references/")

    manifest = load_manifest(skill_dir, errors)
    if manifest:
        if manifest.get("name") != CANONICAL_NAME:
            errors.append("references/skill_manifest.json name does not match canonical skill name")
        if skill_version and manifest.get("version") != skill_version:
            errors.append("references/skill_manifest.json version does not match SKILL.md metadata.version")
        profiles = manifest.get("runtime_profiles")
        if not isinstance(profiles, dict) or profiles.get("default") != "protocol_gate":
            errors.append("references/skill_manifest.json must declare protocol_gate as default")
        else:
            profile_doc_path = skill_dir / "references" / "runtime_profiles.md"
            profile_doc = (
                profile_doc_path.read_text(encoding="utf-8")
                if profile_doc_path.is_file()
                else ""
            )
            for profile in ["protocol_gate", "protocol_full", "delta_review"]:
                budget = profiles.get(profile)
                if not isinstance(budget, dict):
                    errors.append(f"runtime_profiles.{profile} must be an object with resource budgets")
                    continue
                for field in ["max_reference_files", "max_reference_characters"]:
                    value = budget.get(field)
                    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                        errors.append(f"runtime_profiles.{profile}.{field} must be a positive integer")
                if isinstance(budget, dict):
                    resources = budget.get("baseline_resources")
                    if (
                        not isinstance(resources, list)
                        or not resources
                        or not all(isinstance(item, str) for item in resources)
                        or len(resources) != len(set(resources))
                    ):
                        errors.append(
                            f"runtime_profiles.{profile}.baseline_resources must be a non-empty unique string array"
                        )
                    else:
                        missing = [item for item in resources if not (skill_dir / item).is_file()]
                        if missing:
                            errors.append(
                                f"runtime_profiles.{profile}.baseline_resources are missing: {missing}"
                            )
                        else:
                            character_count = sum(
                                len((skill_dir / item).read_text(encoding="utf-8"))
                                for item in resources
                            )
                            max_files = budget.get("max_reference_files")
                            max_characters = budget.get("max_reference_characters")
                            if isinstance(max_files, int) and len(resources) > max_files:
                                errors.append(
                                    f"runtime_profiles.{profile} baseline exceeds max_reference_files"
                                )
                            if (
                                isinstance(max_characters, int)
                                and character_count > max_characters
                            ):
                                errors.append(
                                    f"runtime_profiles.{profile} baseline exceeds max_reference_characters"
                                )
                    expected_row = (
                        f"| `{profile}` | {budget.get('max_reference_files')} | "
                        f"{budget.get('max_reference_characters')} |"
                    )
                    if expected_row not in profile_doc:
                        errors.append(
                            f"references/runtime_profiles.md budget row is out of sync for {profile}"
                        )

    # Cross-check all manifest and SKILL resource references against actual files.
    declared_resources = manifest_resources(manifest)
    skill_references = referenced_resources_from_skill(skill_text)
    for resource in sorted(declared_resources | skill_references):
        if resource.endswith("/") or resource.endswith("*.schema.json"):
            continue
        if not (skill_dir / resource).exists():
            errors.append(f"Referenced resource is missing: {resource}")

    # `structured_format_resources` is a curated subset of structured templates/schemas,
    # not a complete resource inventory. Missing files are errors; absence from the
    # manifest is not. Full inventory enforcement should use a dedicated
    # `resource_inventory` field in a future schema-compatible release.

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists():
        text = openai_yaml.read_text(encoding="utf-8")
        for required in ["display_name:", "short_description:", "default_prompt:", "allow_implicit_invocation:"]:
            if required not in text:
                errors.append(f"agents/openai.yaml missing {required}")

    version_check = skill_dir / "scripts" / "check_version_consistency.py"
    if version_check.exists():
        result = subprocess.run(
            [sys.executable, str(version_check.resolve()), "--mode", "package"],
            cwd=skill_dir,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            detail = (result.stdout + result.stderr).strip()
            errors.append(f"scripts/check_version_consistency.py failed: {detail}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=Path(CANONICAL_NAME))
    args = parser.parse_args()

    errors = validate_skill(args.skill_dir)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        return 1
    print(f"Installable skill smoke test passed: {args.skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
