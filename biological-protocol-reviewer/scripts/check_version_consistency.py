#!/usr/bin/env python3
"""Check biological-protocol-reviewer version consistency across package files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parent
SKILL_NAME = "biological-protocol-reviewer"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_skill_version(text: str) -> str | None:
    match = re.search(r"metadata:\s*(?:\n\s+[A-Za-z0-9_-]+:.*)*\n\s+version:\s*\"([^\"]+)\"", text)
    if match:
        return match.group(1)
    match = re.search(r"^  version:\s*\"([^\"]+)\"", text, flags=re.MULTILINE)
    return match.group(1) if match else None


def expect_contains(path: Path, marker: str, errors: list[str]) -> None:
    if marker not in read(path):
        errors.append(f"{path.relative_to(REPO_ROOT)} does not contain {marker!r}")


def expect_regex(path: Path, pattern: str, expected: str, errors: list[str]) -> None:
    text = read(path)
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match or match.group(1) != expected:
        errors.append(f"{path.relative_to(REPO_ROOT)} version does not match {expected}")


def main() -> int:
    errors: list[str] = []
    skill_md = read(SKILL_ROOT / "SKILL.md")
    version = extract_skill_version(skill_md)
    if not version:
        errors.append("Could not find metadata.version in SKILL.md")
        version = "UNKNOWN"

    body_version = re.search(r"^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", skill_md, flags=re.MULTILINE)
    if not body_version or body_version.group(1) != version:
        errors.append("SKILL.md body Version does not match metadata.version")

    manifest = json.loads(read(SKILL_ROOT / "references" / "skill_manifest.json"))
    if manifest.get("name") != SKILL_NAME:
        errors.append("references/skill_manifest.json name does not match canonical skill name")
    if manifest.get("version") != version:
        errors.append("references/skill_manifest.json version does not match metadata.version")

    expected = f"{SKILL_NAME} v{version}"
    for relpath in [
        "templates/Review_Report_template.md",
        "templates/protocol_passport_template.yaml",
    ]:
        if expected not in read(SKILL_ROOT / relpath):
            errors.append(f"{relpath} does not contain {expected!r}")

    expect_regex(REPO_ROOT / "pyproject.toml", r'^version\s*=\s*"([^"]+)"', version, errors)
    expect_contains(REPO_ROOT / "README.md", f"Version-v{version}", errors)
    expect_contains(REPO_ROOT / "README.zh-CN.md", f"Version-v{version}", errors)
    expect_contains(REPO_ROOT / "CHANGELOG.md", f"## v{version} -", errors)

    stale_markers = ["1.3.2", "Biological-Protocol-Reviewer"]
    for path in SKILL_ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.name == "check_version_consistency.py":
            continue
        if path.suffix in {".pyc", ".png", ".jpg", ".jpeg", ".pdf"}:
            continue
        text = read(path)
        for marker in stale_markers:
            if marker in text:
                errors.append(f"stale marker {marker!r} found in {path.relative_to(SKILL_ROOT)}")

    if errors:
        for error in errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        return 1
    print(f"Version consistency passed: {SKILL_NAME} v{version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
