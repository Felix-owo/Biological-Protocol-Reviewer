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

REQUIRED_REPORT = [
    "Protocol",
    "Protocol重建",
    "执行摘要",
    "成熟度",
    "Module activation",
    "Evidence benchmark",
    "Protocol Readiness Contract",
    "Parameter authority",
    "Readout contracts",
    "Protocol panel synthesis",
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
    "Operator burden",
    "mini-pilot",
    "Original-to-revised",
    "Red-line self-audit",
]

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

ISSUE_REQUIRED_LABELS = [
    "具体问题",
    "证据",
    "影响",
    "解决",
    "决定性 readout",
    "SOP修订位置",
]

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
    for (prev_item, prev_pos), (item, pos) in zip(positions, positions[1:], strict=False):
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


def extract_issue_blocks(text: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"(?ms)^###\s+((?:C|M)\d+)\.?[^\n]*\n(?P<body>.*?)(?=^###\s+|^##\s+|\Z)")
    blocks: list[tuple[str, str]] = []
    for match in pattern.finditer(text):
        issue_id = match.group(1)
        body = match.group("body")
        # Ignore untouched template placeholders with no issue title/content.
        if "<" in match.group(0) and "具体问题" in body and not re.search(r"\S{8,}", body.replace("具体问题", "")):
            continue
        blocks.append((issue_id, body))
    return blocks


def issue_block_errors(report_text: str) -> list[str]:
    errors: list[str] = []
    for issue_id, body in extract_issue_blocks(report_text):
        missing = [label for label in ISSUE_REQUIRED_LABELS if label not in body]
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


def traceability_errors(report_text: str) -> list[str]:
    errors: list[str] = []
    issues = extract_issue_blocks(report_text)
    if not issues:
        return errors
    mapping = section_after(report_text, "Review-to-SOP mapping")
    if not mapping:
        errors.append("Review-to-SOP mapping section is missing while Critical/Major issues exist")
        return errors
    for issue_id, _ in issues:
        if issue_id not in mapping:
            errors.append(f"{issue_id}: missing from Review-to-SOP mapping")
    required_mapping_terms = ["SOP", "Revision", "Status"]
    for term in required_mapping_terms:
        if term.lower() not in mapping.lower():
            errors.append(f"Review-to-SOP mapping appears incomplete; missing {term!r}")
    return errors


def confirmation_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    for match in re.finditer(r"△?TO BE CONFIRMED", text):
        start = max(0, match.start() - 100)
        end = min(len(text), match.end() + 160)
        window = text[start:end]
        if not re.search(r"who|owner|confirm|确认|负责人|由.*确认|confirmation", window, flags=re.I):
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
    parser.add_argument("--report", type=Path, help="Path to Review_Report.md")
    parser.add_argument("--protocol", type=Path, help="Path to Revised_Protocol.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--strict-content",
        action="store_true",
        help="Promote traceability warnings for TO BE CONFIRMED/QC gates to errors.",
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
        miss = missing_required(report_text, REQUIRED_REPORT)
        errors.extend([f"Review_Report missing required content: {x}" for x in miss])
        errors.extend(issue_block_errors(report_text))
        errors.extend(traceability_errors(report_text))

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
    if args.strict_content:
        promoted = [warning for warning in warnings if "TO BE CONFIRMED" in warning or "QC content" in warning]
        errors.extend(promoted)
        warnings = [warning for warning in warnings if warning not in promoted]

    result = {
        "ok": not errors,
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
