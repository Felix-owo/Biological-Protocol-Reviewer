#!/usr/bin/env python3
"""Validate Biological-Protocol-Reviewer outputs.

This script performs deterministic structural checks. It does not replace
scientific review or rendered DOCX visual QA.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


REQUIRED_REPORT = [
    "Protocol",
    "Protocol重建",
    "执行摘要",
    "成熟度",
    "Module activation",
    "Evidence benchmark",
    "Severity-ranked",
    "具体问题",
    "证据",
    "影响",
    "解决",
    "决定性 readout",
    "QC",
    "Metadata",
    "统计",
    "安全",
    "Assumption",
    "Parameter provenance",
    "Operator burden",
    "mini-pilot",
    "Original-to-revised",
    "Red-line self-audit",
]

REQUIRED_DOCX = [
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


def read_docx_text(path: Path) -> tuple[str, list[str]]:
    problems: list[str] = []
    if not path.exists():
        return "", [f"Missing DOCX: {path}"]
    try:
        with ZipFile(path) as zf:
            xml = zf.read("word/document.xml")
    except Exception as exc:  # pragma: no cover - defensive
        return "", [f"Cannot read DOCX: {exc}"]

    root = ET.fromstring(xml)
    parts: list[str] = []
    for t in root.findall(".//w:t", NS):
        if t.text:
            parts.append(t.text)
    return "\n".join(parts), problems


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
    for (prev_item, prev_pos), (item, pos) in zip(positions, positions[1:]):
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, help="Path to Review_Report.md")
    parser.add_argument("--docx", type=Path, help="Path to Revised_Protocol.docx")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    report_text, report_read_errors = read_text(args.report)
    docx_text, docx_read_errors = read_docx_text(args.docx) if args.docx else ("", [])
    all_text = "\n".join([report_text, docx_text])

    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(report_read_errors)
    errors.extend(docx_read_errors)

    if args.report:
        miss = missing_required(report_text, REQUIRED_REPORT)
        errors.extend([f"Review_Report missing required content: {x}" for x in miss])

    if args.docx:
        miss = missing_required(docx_text, REQUIRED_DOCX)
        errors.extend([f"Revised_Protocol.docx missing required content: {x}" for x in miss])
        errors.extend(order_errors(docx_text, MAIN_BODY_ORDER))

    hits = vague_hits(all_text)
    if hits:
        errors.append(f"Unresolved vague language found ({len(hits)} examples)")
        warnings.extend(hits[:10])

    if recommended_without_provenance(all_text):
        errors.append("Recommended parameters are present without parameter provenance/source table")

    if "△TO BE CONFIRMED" in all_text and "who" not in all_text.lower() and "确认" not in all_text:
        warnings.append("TO BE CONFIRMED items may not state who/what must confirm them")

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
