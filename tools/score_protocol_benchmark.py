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
READINESS_RANGES = {
    "Level 0": (0.0, 3.9),
    "Level 1": (4.0, 5.9),
    "Level 2": (6.0, 7.9),
    "Level 3": (8.0, 10.0),
}
ISSUE_HEADING = re.compile(
    r"(?ms)^#{2,6}\s+(?P<label>C\d+|M\d+|m\d+|O\d+|Critical|Major|Minor|Optimization)"
    r"(?:\.|\b)[^\n]*\n(?P<body>.*?)(?=^#{2,6}\s+|\Z)"
)
REASONING_FIELDS = {
    "problem": ("具体问题", "specific problem", "issue"),
    "evidence": ("证据", "evidence"),
    "impact": ("影响", "impact"),
    "resolution": ("解决", "resolution"),
    "decisive_readout": ("决定性 readout", "decisive readout", "acceptance criterion"),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def issue_severity(label: str) -> str:
    if label.startswith("C") or label == "Critical":
        return "Critical"
    if label.startswith("M") or label == "Major":
        return "Major"
    if label.startswith("m") or label == "Minor":
        return "Minor"
    return "Optimization"


def field_content(body: str, aliases: tuple[str, ...]) -> str | None:
    alias_pattern = "|".join(re.escape(alias) for alias in aliases)
    pattern = re.compile(
        rf"(?:\*\*)?(?:{alias_pattern})\s*[:：](?:\*\*)?\s*(?P<value>[^\n]+)",
        flags=re.IGNORECASE,
    )
    for match in pattern.finditer(body):
        value = re.sub(r"<[^>]*>", "", match.group("value")).strip(" *_-|")
        if len(value) >= 4:
            return value
    return None


def reasoned_finding_blocks(text: str) -> list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    for match in ISSUE_HEADING.finditer(text):
        body = match.group("body")
        fields = {
            name: field_content(body, aliases)
            for name, aliases in REASONING_FIELDS.items()
        }
        if all(fields.values()):
            blocks.append(
                {
                    "finding_id": f"F{len(blocks) + 1}",
                    "severity": issue_severity(match.group("label")),
                    "body": body,
                    "fields": fields,
                }
            )
    return blocks


def extract_readiness(text: str) -> tuple[float | None, str | None, str | None]:
    score_patterns = [
        r"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?(?:readiness score|准备度评分|就绪评分)"
        r"(?:\*\*)?\s*[:：]\s*([^\n]+)$",
        r"(?im)^\s*\|\s*(?:readiness score|准备度评分|就绪评分)\s*\|\s*"
        r"([^|]+)\|",
    ]
    level_patterns = [
        r"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?(?:maturity level|当前成熟度|成熟度)"
        r"(?:\*\*)?\s*[:：]\s*([^\n]+)$",
        r"(?im)^\s*\|\s*(?:maturity level|当前成熟度|成熟度)\s*\|\s*"
        r"([^|]+)\|",
    ]
    score_value: str | None = None
    level_value: str | None = None
    for pattern in score_patterns:
        match = re.search(pattern, text)
        if match:
            score_value = match.group(1).strip().strip(" *_`|。.;；")
            break
    for pattern in level_patterns:
        match = re.search(pattern, text)
        if match:
            level_value = match.group(1).strip().strip(" *_`|。.;；")
            break
    if score_value is None or level_value is None:
        return None, None, "explicit 0-10 readiness score and maturity level are required"
    if re.search(r"<[^>]+>|\b(?:TBD|TBC|placeholder)\b", score_value, re.I):
        return None, None, "readiness score must not be a placeholder"
    if re.search(r"\d(?:\.\d+)?\s*[-–—]\s*\d", score_value):
        return None, None, "readiness score must be one value, not a range"
    score_match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*(?:/\s*(\d+(?:\.\d+)?))?", score_value)
    if not score_match:
        return None, None, "readiness score must be one numeric value on the 0-10 scale"
    denominator = score_match.group(2)
    if denominator is not None and float(denominator) != 10:
        return None, None, "readiness score denominator must be /10"
    if re.search(r"<[^>]+>|/|\b(?:TBD|TBC|placeholder)\b", level_value, re.I):
        return None, None, "maturity level must be one value, not a template list"
    level_match = re.fullmatch(r"Level\s*([0-3])", level_value, re.I)
    if not level_match:
        return None, None, "maturity level must be exactly Level 0, Level 1, Level 2, or Level 3"
    return float(score_match.group(1)), f"Level {level_match.group(1)}", None


def readiness_contract(text: str) -> tuple[bool, float | None, str | None, str | None]:
    score, level, parse_error = extract_readiness(text)
    if score is None or level is None:
        return False, score, level, parse_error
    if not 0 <= score <= 10:
        return False, score, level, "readiness score must be within 0-10"
    minimum, maximum = READINESS_RANGES[level]
    if not minimum <= score <= maximum:
        return False, score, level, f"readiness score {score:g} is inconsistent with {level}"
    return True, score, level, None


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
    sections = [term for term in required_sections if normalize(term) in lowered]
    readiness_ok, readiness_score, maturity_level, readiness_error = readiness_contract(text)
    forbidden_levels = [
        level
        for level in spec.get("forbidden_readiness_levels", [])
        if level == maturity_level
    ]
    min_severity = spec.get("minimum_severity", "Optimization")
    findings = reasoned_finding_blocks(text)
    concept_links = []
    detected = []
    for term in must_detect:
        candidates = []
        for finding in findings:
            field_text = " ".join(str(value) for value in finding["fields"].values())
            if normalize(term) not in normalize(field_text):
                continue
            severity = str(finding["severity"])
            candidates.append(
                {
                    "finding_id": finding["finding_id"],
                    "severity": severity,
                    "severity_ok": (
                        VALID_SEVERITIES[severity] >= VALID_SEVERITIES[min_severity]
                    ),
                }
            )
        qualifying = next((item for item in candidates if item["severity_ok"]), None)
        if qualifying:
            detected.append(term)
        concept_links.append(
            {
                "concept": term,
                "matched": qualifying is not None,
                "linked_finding": qualifying,
                "candidate_findings": candidates,
            }
        )
    severity_ok = bool(must_detect) and all(item["matched"] for item in concept_links)
    behavioral_structure_ok = bool(findings)
    return {
        "detected": detected,
        "must_detect_recall": len(detected) / len(must_detect) if must_detect else 1.0,
        "concept_links": concept_links,
        "required_sections_found": sections,
        "section_recall": len(sections) / len(required_sections) if required_sections else 1.0,
        "severity_ok": severity_ok,
        "reasoned_finding_count": len(findings),
        "behavioral_structure_ok": behavioral_structure_ok,
        "readiness_score": readiness_score,
        "maturity_level": maturity_level,
        "readiness_contract_ok": readiness_ok,
        "readiness_error": readiness_error,
        "forbidden_readiness_levels_found": forbidden_levels,
        "pass": (
            len(detected) == len(must_detect)
            and len(sections) == len(required_sections)
            and severity_ok
            and behavioral_structure_ok
            and readiness_ok
            and not forbidden_levels
        ),
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
