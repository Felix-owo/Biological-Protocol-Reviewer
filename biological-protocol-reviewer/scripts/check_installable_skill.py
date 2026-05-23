#!/usr/bin/env python3
"""Smoke-test the installable biological-protocol-reviewer skill folder."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CANONICAL_NAME = "biological-protocol-reviewer"
REQUIRED_DIRS = ["agents", "examples", "references", "schemas", "scripts", "templates"]
ALLOWED_TOP_LEVEL = {"SKILL.md", *REQUIRED_DIRS}
REQUIRED_FILES = [
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
    "schemas/external_companion_evidence.schema.json",
    "scripts/protocol_output_validator.py",
    "scripts/lint_structured_protocol.py",
    "scripts/check_installable_skill.py",
    "scripts/check_version_consistency.py",
    "scripts/run_regression_fixtures.py",
]
DESCRIPTION_TERMS = ["protocol", "SOP", "QC", "benchmark", "readiness"]
ALLOWED_LICENSES = {"MPL-2.0"}


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


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    if not skill_dir.exists():
        return [f"Skill directory does not exist: {skill_dir}"]
    if skill_dir.name != CANONICAL_NAME:
        errors.append(f"Skill directory must be named {CANONICAL_NAME!r}")

    top_level = {path.name for path in skill_dir.iterdir()}
    unexpected = sorted(top_level - ALLOWED_TOP_LEVEL)
    if unexpected:
        errors.append(f"Unexpected top-level files/directories: {unexpected}")

    for dirname in REQUIRED_DIRS:
        if not (skill_dir / dirname).is_dir():
            errors.append(f"Missing required directory: {dirname}")
    for filename in REQUIRED_FILES:
        if not (skill_dir / filename).is_file():
            errors.append(f"Missing required file: {filename}")
    if (skill_dir / "validators").exists():
        errors.append("Do not keep a top-level validators/ directory; use references/ or scripts/")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8")
        try:
            meta, _ = parse_frontmatter(text)
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

        if "validators/revised_protocol_qc_checklist.md" in text:
            errors.append("SKILL.md still references non-standard validators/ path")
        if "references/revised_protocol_qc_checklist.md" not in text:
            errors.append("SKILL.md must route the revised-protocol QC checklist from references/")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists():
        text = openai_yaml.read_text(encoding="utf-8")
        for required in ["display_name:", "short_description:", "default_prompt:", "allow_implicit_invocation:"]:
            if required not in text:
                errors.append(f"agents/openai.yaml missing {required}")

    version_check = skill_dir / "scripts" / "check_version_consistency.py"
    if version_check.exists():
        result = subprocess.run(
            [sys.executable, str(version_check.resolve())],
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
