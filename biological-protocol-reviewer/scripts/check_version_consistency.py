#!/usr/bin/env python3
"""Check package or release-repository version consistency.

Package mode is self-contained and is safe to run after the installable skill
has been copied to an arbitrary cache directory. Release mode adds repository
metadata checks and is the mode used by CI before publishing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "biological-protocol-reviewer"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_skill_version(text: str) -> str | None:
    match = re.search(r"metadata:\s*(?:\n\s+[A-Za-z0-9_-]+:.*)*\n\s+version:\s*\"([^\"]+)\"", text)
    if match:
        return match.group(1)
    match = re.search(r"^  version:\s*\"([^\"]+)\"", text, flags=re.MULTILINE)
    return match.group(1) if match else None


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def expect_contains(path: Path, marker: str, errors: list[str], root: Path) -> None:
    if not path.is_file():
        errors.append(f"{display_path(path, root)} is missing")
    elif marker not in read(path):
        errors.append(f"{display_path(path, root)} does not contain {marker!r}")


def expect_regex(
    path: Path,
    pattern: str,
    expected: str,
    errors: list[str],
    root: Path,
) -> None:
    if not path.is_file():
        errors.append(f"{display_path(path, root)} is missing")
        return
    text = read(path)
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match or match.group(1) != expected:
        errors.append(f"{display_path(path, root)} version does not match {expected}")


def check_package(skill_root: Path) -> tuple[str, list[str]]:
    errors: list[str] = []
    skill_md_path = skill_root / "SKILL.md"
    if not skill_md_path.is_file():
        return "UNKNOWN", ["SKILL.md is missing"]
    skill_md = read(skill_md_path)
    version = extract_skill_version(skill_md)
    if not version:
        errors.append("Could not find metadata.version in SKILL.md")
        version = "UNKNOWN"

    body_version = re.search(r"^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", skill_md, flags=re.MULTILINE)
    if not body_version or body_version.group(1) != version:
        errors.append("SKILL.md body Version does not match metadata.version")

    manifest_path = skill_root / "references" / "skill_manifest.json"
    try:
        manifest = json.loads(read(manifest_path))
    except Exception as exc:
        errors.append(f"Could not parse references/skill_manifest.json: {exc}")
    else:
        if manifest.get("name") != SKILL_NAME:
            errors.append("references/skill_manifest.json name does not match canonical skill name")
        if manifest.get("version") != version:
            errors.append("references/skill_manifest.json version does not match metadata.version")

    expected = f"{SKILL_NAME} v{version}"
    for relpath in [
        "templates/Review_Report_template.md",
        "templates/protocol_passport_template.yaml",
    ]:
        path = skill_root / relpath
        if not path.is_file():
            errors.append(f"{relpath} is missing")
        elif expected not in read(path):
            errors.append(f"{relpath} does not contain {expected!r}")

    agent_metadata = skill_root / "agents" / "openai.yaml"
    expect_regex(
        agent_metadata,
        r'^\s*display_name:.*v([0-9]+\.[0-9]+\.[0-9]+)',
        version,
        errors,
        skill_root,
    )
    expect_regex(
        agent_metadata,
        r'^\s*default_prompt:.*v([0-9]+\.[0-9]+\.[0-9]+)',
        version,
        errors,
        skill_root,
    )

    stale_markers = ["1.3.2", "1.4.2", "Biological-Protocol-Reviewer"]
    for path in skill_root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.name == "check_version_consistency.py":
            continue
        if path.suffix in {".pyc", ".png", ".jpg", ".jpeg", ".pdf"}:
            continue
        text = read(path)
        for marker in stale_markers:
            if marker in text:
                errors.append(f"stale marker {marker!r} found in {path.relative_to(skill_root)}")

    return version, errors


def check_release(repo_root: Path, version: str) -> list[str]:
    errors: list[str] = []
    expect_regex(
        repo_root / "pyproject.toml",
        r'^version\s*=\s*"([^"]+)"',
        version,
        errors,
        repo_root,
    )
    expect_contains(repo_root / "README.md", f"Version-v{version}", errors, repo_root)
    expect_contains(repo_root / "README.zh-CN.md", f"Version-v{version}", errors, repo_root)
    expect_contains(repo_root / "CHANGELOG.md", f"## v{version} -", errors, repo_root)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["package", "release"], default="package")
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root for release mode (defaults to the package parent).",
    )
    args = parser.parse_args()

    version, errors = check_package(SKILL_ROOT)
    if args.mode == "release":
        repo_root = (args.repo_root or SKILL_ROOT.parent).resolve()
        errors.extend(check_release(repo_root, version))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        return 1
    print(f"Version consistency passed ({args.mode}): {SKILL_NAME} v{version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
