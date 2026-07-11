#!/usr/bin/env python3
"""Validate biological-protocol-reviewer Markdown outputs.

This script performs deterministic structural checks. It does not replace
scientific review, but it catches empty-shell outputs, unresolved vague language,
and missing traceability in Critical/Major issue blocks.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BASE_REQUIRED_REPORT = [
    "Protocol",
    "Protocol重建",
    "执行摘要",
    "成熟度",
    "Module activation",
    "Evidence benchmark",
    "Protocol Readiness Contract",
    "Parameter authority",
    "Readout contracts",
    "Severity-ranked",
    "具体问题",
    "证据",
    "影响",
    "解决",
    "决定性 readout",
    "QC",
    "Metadata",
    "Data records and repository gate",
    "统计",
    "安全",
    "Assumption",
    "Parameter provenance",
    "Red-line self-audit",
]

FULL_REQUIRED_REPORT = [
    "Protocol panel synthesis",
    "Operator burden",
    "mini-pilot",
    "Original-to-revised",
    "Review-to-SOP mapping",
]

DELTA_TRACE_LABELS = [
    "Prior review ID",
    "Changed artifact IDs",
    "Prior open finding IDs",
    "Resolved finding IDs",
    "New finding IDs",
    "Carried-forward finding IDs",
]
RUNTIME_PROFILES = {"protocol_gate", "protocol_full", "delta_review"}
PROFILE_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:\*\*Runtime profile[:：]\*\*|Runtime profile\s*[:：])\s*"
    r"`?(protocol_gate|protocol_full|delta_review)`?\s*[.。]?\s*$"
)

REQUIRED_PROTOCOL = [
    "文档控制",
    "SOP快速执行摘要",
    "开始前准备",
    "实验步骤",
    "试剂配制",
    "试剂、耗材、仪器",
    "质量控制",
    "时间安排",
    "暂停点",
    "疑难排查",
    "预期结果",
    "数据分析",
    "附录A",
    "附录B",
    "附录C",
    "附录D",
    "附录E",
    "附录F",
    "附录G",
    "附录H",
    "附录I",
    "附录J",
    "附录K",
]

MAIN_BODY_ORDER = [
    "SOP快速执行摘要",
    "开始前准备",
    "实验步骤",
    "试剂配制",
    "质量控制",
    "疑难排查",
]

ISSUE_REQUIRED_LABELS = {
    "specific problem": ("具体问题", "Specific problem"),
    "evidence": ("证据", "Evidence"),
    "impact": ("影响", "Impact"),
    "resolution": ("解决", "Resolution"),
    "decisive readout": ("决定性 readout", "Decisive readout"),
    "SOP location": ("SOP修订位置", "SOP location"),
}

VAGUE_PATTERNS = [
    r"appropriate amount",
    r"as needed",
    r"standard protocol",
    r"standard conditions",
    r"follow kit instructions",
    r"optimi[sz]e if necessary",
    r"sufficient volume",
    r"suitable concentration",
    r"room temperature(?![^\\n。；;]{0,40}(range|范围|记录|20|25|℃|°C))",
    r"briefly",
    r"carefully(?![^\\n。；;]{0,40}(avoid|防止|确保|指定|specif))",
    r"适量",
    r"适当",
    r"按需",
    r"标准流程",
    r"标准条件",
    r"按照试剂盒说明(?![^\\n。；;]{0,80}(版本|步骤|参数|记录|TO BE CONFIRMED))",
    r"室温(?![^\\n。；;]{0,40}(范围|记录|20|25|℃|°C))",
    r"短暂",
    r"小心(?![^\\n。；;]{0,40}(避免|确保|记录|指定))",
]
READINESS_RANGES = {
    "Level 0": (0.0, 3.9),
    "Level 1": (4.0, 5.9),
    "Level 2": (6.0, 7.9),
    "Level 3": (8.0, 10.0),
}
ALLOWED_BURDEN = {"low", "moderate", "high"}


def read_text(path: Path | None) -> tuple[str, list[str]]:
    if path is None:
        return "", []
    if not path.exists():
        return "", [f"Missing file: {path}"]
    return path.read_text(encoding="utf-8", errors="replace"), []


def missing_required(text: str, required: list[str]) -> list[str]:
    return [item for item in required if item not in text]


def order_errors(text: str, ordered: list[str]) -> list[str]:
    positions = []
    for item in ordered:
        pos = text.find(item)
        if pos == -1:
            continue
        positions.append((item, pos))
    errors = []
    for index in range(1, len(positions)):
        prev_item, prev_pos = positions[index - 1]
        item, pos = positions[index]
        if pos < prev_pos:
            errors.append(f"Section order problem: {item} appears before {prev_item}")
    return errors


def vague_hits(text: str) -> list[str]:
    hits = []
    for pattern in VAGUE_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            start = max(0, match.start() - 45)
            end = min(len(text), match.end() + 80)
            window = text[start:end].replace("\n", " ")
            if "TO BE CONFIRMED" in window or "△TO BE CONFIRMED" in window:
                continue
            hits.append(window)
            if len(hits) >= 30:
                return hits
    return hits


def recommended_without_provenance(text: str) -> bool:
    if "★RECOMMENDED" not in text and "RECOMMENDED — TO BE VERIFIED LOCALLY" not in text:
        return False
    provenance_terms = [
        "Parameter provenance",
        "参数溯源",
        "Source and citation",
        "来源与引用",
        "PMID",
        "DOI",
        "manual version",
        "Access date",
    ]
    return not any(term in text for term in provenance_terms)


def _label_value(text: str, aliases: tuple[str, ...]) -> str | None:
    alias_pattern = "|".join(re.escape(alias) for alias in aliases)
    patterns = [
        re.compile(
            rf"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?(?:{alias_pattern})(?:\*\*)?"
            r"\s*[:：]\s*(?P<value>[^\n]+)$"
        ),
        re.compile(
            rf"(?im)^\s*\|\s*(?:{alias_pattern})\s*\|\s*(?P<value>[^|]+)\|"
        ),
    ]
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            return match.group("value").strip().strip(" *_`|。.;；")
    return None


def readiness_errors(report_text: str) -> list[str]:
    score_value = _label_value(report_text, ("readiness score", "准备度评分", "就绪评分"))
    level_value = _label_value(report_text, ("maturity level", "当前成熟度", "成熟度"))
    if score_value is None or level_value is None:
        return ["Review_Report must state an explicit 0-10 readiness score and Level 0-3 maturity"]

    if re.search(r"<[^>]+>|\b(?:TBD|TBC|placeholder)\b", score_value, re.I):
        return ["Readiness score must be a completed single 0-10 value, not a placeholder"]
    if re.search(r"\d(?:\.\d+)?\s*[-–—]\s*\d", score_value):
        return ["Readiness score must be one value, not a range"]
    score_match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*(?:/\s*(\d+(?:\.\d+)?))?", score_value)
    if not score_match:
        return ["Readiness score must be one numeric value on the 0-10 scale"]
    denominator = score_match.group(2)
    if denominator is not None and float(denominator) != 10:
        return ["Readiness score denominator must be /10; /100 and other scales are invalid"]
    score = float(score_match.group(1))

    if re.search(r"<[^>]+>|/|\b(?:TBD|TBC|placeholder)\b", level_value, re.I):
        return ["Maturity level must be one completed Level 0-3 value, not a template list"]
    level_match = re.fullmatch(r"Level\s*([0-3])", level_value, re.I)
    if not level_match:
        return ["Maturity level must be exactly one of Level 0, Level 1, Level 2, or Level 3"]
    level = f"Level {level_match.group(1)}"

    if not 0 <= score <= 10:
        return ["Readiness score must be within 0-10"]
    minimum, maximum = READINESS_RANGES[level]
    if not minimum <= score <= maximum:
        return [f"Readiness score {score:g} is inconsistent with {level}"]
    return []


def extract_issue_blocks(text: str) -> list[tuple[str, str]]:
    pattern = re.compile(
        r"(?ms)^###\s+(?:(?P<direct>[CM]\d+)\.?|"
        r"(?:Critical|Major)(?:\s+issue)?\s+(?P<named>[CM]\d+))"
        r"[^\n]*\n(?P<body>.*?)(?=^###\s+|^##\s+|\Z)"
    )
    blocks: list[tuple[str, str]] = []
    for match in pattern.finditer(text):
        issue_id = match.group("direct") or match.group("named")
        body = match.group("body")
        # Ignore untouched template placeholders with no issue title/content.
        if "<" in match.group(0) and "具体问题" in body and not re.search(r"\S{8,}", body.replace("具体问题", "")):
            continue
        blocks.append((issue_id, body))
    return blocks


def issue_block_errors(report_text: str) -> list[str]:
    errors: list[str] = []
    for issue_id, body in extract_issue_blocks(report_text):
        missing = [
            label
            for label, aliases in ISSUE_REQUIRED_LABELS.items()
            if not any(re.search(rf"{re.escape(alias)}\s*[:：]", body, re.I) for alias in aliases)
        ]
        if missing:
            errors.append(f"{issue_id}: Critical/Major issue block missing labels: {', '.join(missing)}")
        if not re.search(r"failure mode|失败模式|伪阳性|伪阴性|批次效应|污染|偏倚|执行偏差", body, flags=re.I):
            errors.append(f"{issue_id}: issue block does not name a concrete failure mode or alternative error mode")
    return errors


def section_after(text: str, title: str) -> str:
    idx = text.find(title)
    if idx == -1:
        return ""
    rest = text[idx:]
    next_match = re.search(r"\n##\s+", rest[len(title):])
    if not next_match:
        return rest
    return rest[: len(title) + next_match.start()]


def traceability_errors(report_text: str, require_mapping: bool) -> list[str]:
    errors: list[str] = []
    issues = extract_issue_blocks(report_text)
    if not issues:
        return errors
    mapping = section_after(report_text, "Review-to-SOP mapping")
    if not mapping:
        if require_mapping:
            errors.append("Review-to-SOP mapping section is required for protocol_full")
        return errors
    for issue_id, _ in issues:
        if issue_id not in mapping:
            errors.append(f"{issue_id}: missing from Review-to-SOP mapping")
    required_mapping_terms = ["SOP", "Revision", "Status"]
    for term in required_mapping_terms:
        if term.lower() not in mapping.lower():
            errors.append(f"Review-to-SOP mapping appears incomplete; missing {term!r}")
    return errors


def profile_errors(report_text: str, profile: str, protocol_supplied: bool) -> list[str]:
    errors: list[str] = []
    match = PROFILE_RE.search(report_text)
    if not match:
        errors.append("Review_Report must state `Runtime profile: <profile>`")
    elif match.group(1) != profile:
        errors.append(
            f"Review_Report runtime profile `{match.group(1)}` does not match --profile {profile}"
        )

    if profile == "protocol_full" and not protocol_supplied:
        errors.append("protocol_full requires --protocol Revised_Protocol.md")
    if profile in {"protocol_gate", "delta_review"} and protocol_supplied:
        errors.append(f"{profile} is review-only; use protocol_full to validate a rewritten SOP")
    return errors


def _section_by_heading(text: str, title: str) -> str:
    pattern = re.compile(rf"(?im)^##\s+[^\n]*{re.escape(title)}[^\n]*$")
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"(?m)^##\s+", text[start:])
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end]


def operator_burden_errors(report_text: str, required: bool) -> list[str]:
    section = _section_by_heading(report_text, "Operator burden")
    if not section:
        return ["protocol_full requires an Operator burden budget section"] if required else []

    table_rows = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip().strip(" *_`") for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        table_rows.append(cells)
    if not table_rows:
        return ["Operator burden section must contain a burden table"]
    header = [cell.casefold() for cell in table_rows[0]]
    try:
        burden_index = header.index("burden")
    except ValueError:
        return ["Operator burden table must contain a `Burden` column"]

    errors: list[str] = []
    data_rows = [row for row in table_rows[1:] if any(cell for cell in row)]
    if not data_rows:
        return ["Operator burden table must contain at least one completed row"]
    for row_index, row in enumerate(data_rows, start=1):
        burden = row[burden_index].casefold() if burden_index < len(row) else ""
        if burden not in ALLOWED_BURDEN:
            errors.append(
                f"Operator burden row {row_index} must use low, moderate, or high; got {burden!r}"
            )
    return errors


def _delta_list(report_text: str, label: str) -> list[str] | None:
    value = _label_value(report_text, (label,))
    if value is None:
        return None
    if value.casefold() in {"none", "无", "n/a", "not applicable"}:
        return []
    return [item.strip() for item in re.split(r"[,，;；]", value) if item.strip()]


def delta_trace_errors(report_text: str) -> list[str]:
    errors = [
        f"delta_review missing required trace field: {label}"
        for label in DELTA_TRACE_LABELS
        if _label_value(report_text, (label,)) is None
    ]
    if errors:
        return errors

    prior_review = _label_value(report_text, ("Prior review ID",)) or ""
    changed = _delta_list(report_text, "Changed artifact IDs") or []
    prior_open = _delta_list(report_text, "Prior open finding IDs") or []
    resolved = _delta_list(report_text, "Resolved finding IDs") or []
    new = _delta_list(report_text, "New finding IDs") or []
    carried = _delta_list(report_text, "Carried-forward finding IDs") or []
    if len(prior_review) < 3:
        errors.append("delta_review Prior review ID must be substantive")
    if not changed:
        errors.append("delta_review Changed artifact IDs must be non-empty")
    if not prior_open:
        errors.append("delta_review Prior open finding IDs must be non-empty")
    for label, values in [
        ("Changed artifact IDs", changed),
        ("Prior open finding IDs", prior_open),
        ("Resolved finding IDs", resolved),
        ("New finding IDs", new),
        ("Carried-forward finding IDs", carried),
    ]:
        if len(values) != len(set(values)):
            errors.append(f"delta_review {label} must contain unique IDs")
    prior_set = set(prior_open)
    resolved_set = set(resolved)
    carried_set = set(carried)
    if resolved_set & carried_set:
        errors.append("delta_review resolved and carried-forward finding IDs must be disjoint")
    if prior_set != resolved_set | carried_set:
        errors.append(
            "delta_review prior open IDs must equal resolved plus carried-forward IDs"
        )
    if set(new) & prior_set:
        errors.append("delta_review new finding IDs must not reuse prior open IDs")
    return errors


def confirmation_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    for match in re.finditer(r"△?TO BE CONFIRMED", text):
        start = max(0, match.start() - 100)
        end = min(len(text), match.end() + 160)
        context = text[start:match.start()] + text[match.end():end]
        if not re.search(r"who|owner|confirm|确认|负责人|由.*确认|confirmation", context, flags=re.I):
            warnings.append("TO BE CONFIRMED item may lack confirmation owner/context")
            break
    return warnings


def qc_gate_warnings(report_text: str, protocol_text: str) -> list[str]:
    text = "\n".join([report_text, protocol_text])
    warnings: list[str] = []
    if "QC" in text or "质量控制" in text:
        if not re.search(r"acceptance criterion|接受标准|判定标准|threshold|阈值", text, flags=re.I):
            warnings.append("QC content may lack explicit acceptance criteria/thresholds")
        if not re.search(r"fail action|失败处理|stop/go|repeat|rescue|exclusion|排除|重复|补救", text, flags=re.I):
            warnings.append("QC content may lack fail action, stop/go, repeat, rescue, or exclusion rule")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        required=True,
        choices=sorted(RUNTIME_PROFILES),
        help="Runtime profile whose Markdown output contract must be enforced.",
    )
    parser.add_argument("--report", type=Path, help="Path to Review_Report.md")
    parser.add_argument("--protocol", type=Path, help="Path to Revised_Protocol.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    content_mode = parser.add_mutually_exclusive_group()
    content_mode.add_argument(
        "--strict-content",
        action="store_true",
        help="Compatibility flag; strict content checks are enabled by default.",
    )
    content_mode.add_argument(
        "--lenient-content",
        action="store_true",
        help="Keep TO BE CONFIRMED/QC traceability diagnostics as warnings for legacy non-decision drafts.",
    )
    args = parser.parse_args()

    report_text, report_read_errors = read_text(args.report)
    protocol_text, protocol_read_errors = read_text(args.protocol)
    all_text = "\n".join([report_text, protocol_text])

    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(report_read_errors)
    errors.extend(protocol_read_errors)

    if args.report:
        errors.extend(profile_errors(report_text, args.profile, args.protocol is not None))
        required_report = BASE_REQUIRED_REPORT + (
            FULL_REQUIRED_REPORT if args.profile == "protocol_full" else []
        )
        miss = missing_required(report_text, required_report)
        errors.extend([f"Review_Report missing required content: {x}" for x in miss])
        errors.extend(readiness_errors(report_text))
        errors.extend(issue_block_errors(report_text))
        errors.extend(
            traceability_errors(report_text, require_mapping=args.profile == "protocol_full")
        )
        errors.extend(
            operator_burden_errors(report_text, required=args.profile == "protocol_full")
        )
        if args.profile == "delta_review":
            errors.extend(delta_trace_errors(report_text))
    elif args.profile in RUNTIME_PROFILES:
        errors.append(f"{args.profile} requires --report Review_Report.md")

    if args.protocol:
        miss = missing_required(protocol_text, REQUIRED_PROTOCOL)
        errors.extend([f"Revised_Protocol.md missing required content: {x}" for x in miss])
        errors.extend(order_errors(protocol_text, MAIN_BODY_ORDER))

    hits = vague_hits(all_text)
    if hits:
        errors.append(f"Unresolved vague language found ({len(hits)} examples)")
        warnings.extend(hits[:10])

    if recommended_without_provenance(all_text):
        errors.append("Recommended parameters are present without parameter provenance/source table")

    warnings.extend(confirmation_warnings(all_text))
    warnings.extend(qc_gate_warnings(report_text, protocol_text))
    if not args.lenient_content:
        promoted = [warning for warning in warnings if "TO BE CONFIRMED" in warning or "QC content" in warning]
        errors.extend(promoted)
        warnings = [warning for warning in warnings if warning not in promoted]
    else:
        warnings.append(
            "--lenient-content is a legacy draft mode; this output is not decision-eligible"
        )

    result = {
        "ok": not errors,
        "decision_eligible": not errors and not args.lenient_content,
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("OK" if result["ok"] else "FAILED")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARN: {item}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
