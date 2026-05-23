#!/usr/bin/env python3
"""Check and optionally score the biological-protocol-reviewer benchmark set."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VALID_SEVERITIES = {"Critical": 3, "Major": 2, "Minor": 1, "Optimization": 0}
VALID_LEVELS = {"Level 0", "Level 1", "Level 2", "Level 3"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def check_definitions(root: Path) -> list[str]:
    errors: list[str] = []
    expected = load_json(root / "expected_findings.json")
    rubric = load_json(root / "scoring_rubric.json")
    cases_dir = root / "cases"

    weights = rubric.get("score_components", {})
    if not weights or abs(sum(float(v) for v in weights.values()) - 1.0) > 0.001:
        errors.append("scoring_rubric.json score_components must sum to 1.0")

    for case_id, spec in expected.items():
        if not (cases_dir / f"{case_id}.md").exists():
            errors.append(f"{case_id}: missing benchmark case file")
        if not spec.get("must_detect"):
            errors.append(f"{case_id}: must_detect must be non-empty")
        if spec.get("minimum_severity") not in VALID_SEVERITIES:
            errors.append(f"{case_id}: invalid minimum_severity")
        for level in spec.get("forbidden_readiness_levels", []):
            if level not in VALID_LEVELS:
                errors.append(f"{case_id}: invalid forbidden readiness level {level}")
        if not spec.get("required_sop_sections"):
            errors.append(f"{case_id}: required_sop_sections must be non-empty")
    return errors


def score_output(text: str, spec: dict) -> dict:
    lowered = normalize(text)
    must_detect = spec.get("must_detect", [])
    required_sections = spec.get("required_sop_sections", [])
    detected = [term for term in must_detect if normalize(term) in lowered]
    sections = [term for term in required_sections if normalize(term) in lowered]
    forbidden_levels = [level for level in spec.get("forbidden_readiness_levels", []) if normalize(level) in lowered]
    min_severity = spec.get("minimum_severity", "Optimization")
    severity_ok = any(
        normalize(sev) in lowered
        for sev, rank in VALID_SEVERITIES.items()
        if rank >= VALID_SEVERITIES[min_severity]
    )
    return {
        "detected": detected,
        "must_detect_recall": len(detected) / len(must_detect) if must_detect else 1.0,
        "required_sections_found": sections,
        "section_recall": len(sections) / len(required_sections) if required_sections else 1.0,
        "severity_ok": severity_ok,
        "forbidden_readiness_levels_found": forbidden_levels,
        "pass": len(detected) == len(must_detect) and len(sections) == len(required_sections) and severity_ok and not forbidden_levels,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-root", type=Path, default=Path("benchmarks/v1.0"))
    parser.add_argument("--outputs-dir", type=Path, help="Directory containing <case_id>.md model outputs")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors = check_definitions(args.benchmark_root)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        return 1

    if not args.outputs_dir:
        print("Benchmark definitions are valid.")
        return 0

    expected = load_json(args.benchmark_root / "expected_findings.json")
    results = {}
    for case_id, spec in expected.items():
        output_path = args.outputs_dir / f"{case_id}.md"
        if not output_path.exists():
            results[case_id] = {"pass": False, "error": "missing output file"}
            continue
        results[case_id] = score_output(output_path.read_text(encoding="utf-8"), spec)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for case_id, result in results.items():
            status = "PASS" if result.get("pass") else "FAIL"
            print(f"{status} {case_id}: {result}")

    return 0 if all(result.get("pass") for result in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
