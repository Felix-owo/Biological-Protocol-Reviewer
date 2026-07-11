#!/usr/bin/env python3
"""Validate a cross-skill claim-readout handoff artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ALLOWED_ROLES = {"decisive", "supporting", "contextual", "exploratory"}
ALLOWED_AUTHORITY = {
    "original",
    "local_validated",
    "external_benchmark",
    "vendor_manual",
    "institutional_sop",
    "recommended_unvalidated",
    "unresolved",
    "not_applicable",
}
ALLOWED_ACTIONS = {
    "add_control",
    "add_validation",
    "add_qc_gate",
    "narrow_claim",
    "mark_preliminary",
    "author_input_needed",
    "no_action_needed",
}
CONTRACT_VERSION = "1.0.0"
ROOT_REQUIRED_FIELDS = {
    "contract_version",
    "handoff_id",
    "skill_context",
    "claim_readout_map",
}
ROOT_ALLOWED_FIELDS = ROOT_REQUIRED_FIELDS | {"notes", "extensions"}
ITEM_REQUIRED_FIELDS = {
    "claim_id",
    "claim_text",
    "evidence_role",
    "readout_id",
    "readout_supports",
    "protocol_step_or_method",
    "parameter_authority",
    "qc_gate",
    "failure_mode",
    "manuscript_impact",
    "revision_action",
    "source_ids",
}
EXTENSION_NAMESPACES = {"biological_protocol_reviewer", "rigorous_reviewer"}
EXTENSION_FIELDS = {"source_record_ids", "notes"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def substantive(value: Any, min_len: int = 4) -> bool:
    return isinstance(value, str) and len(value.strip()) >= min_len


def validate_unique_ids(value: Any, path: str, require_non_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (require_non_empty and not value):
        qualifier = "non-empty " if require_non_empty else ""
        return [f"{path} must be a {qualifier}array"]
    errors: list[str] = []
    seen: set[str] = set()
    for index, source_id in enumerate(value):
        item_path = f"{path}[{index}]"
        if not substantive(source_id, 2):
            errors.append(f"{item_path} must be a substantive string of at least 2 characters")
            continue
        normalized = source_id.strip()
        if normalized in seen:
            errors.append(f"{item_path} duplicates source ID {normalized!r}")
        seen.add(normalized)
    return errors


def validate_extensions(value: Any) -> list[str]:
    path = "extensions"
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    for field in sorted(set(value) - EXTENSION_NAMESPACES):
        errors.append(f"{path} contains unsupported field `{field}`")
    for namespace in sorted(set(value) & EXTENSION_NAMESPACES):
        namespace_value = value[namespace]
        namespace_path = f"{path}.{namespace}"
        if not isinstance(namespace_value, dict):
            errors.append(f"{namespace_path} must be an object")
            continue
        for field in sorted(set(namespace_value) - EXTENSION_FIELDS):
            errors.append(f"{namespace_path} contains unsupported field `{field}`")
        if "notes" in namespace_value and not isinstance(namespace_value["notes"], str):
            errors.append(f"{namespace_path}.notes must be a string")
        if "source_record_ids" in namespace_value:
            errors.extend(
                validate_unique_ids(
                    namespace_value["source_record_ids"],
                    f"{namespace_path}.source_record_ids",
                    require_non_empty=False,
                )
            )
    return errors


def validate(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["handoff must be a JSON object"]
    errors: list[str] = []
    for field in sorted(ROOT_REQUIRED_FIELDS - set(data)):
        errors.append(f"missing required root field `{field}`")
    for field in sorted(set(data) - ROOT_ALLOWED_FIELDS):
        errors.append(f"root contains unsupported field `{field}`")
    if data.get("contract_version") != CONTRACT_VERSION:
        errors.append(f"contract_version must be {CONTRACT_VERSION!r}")
    if not substantive(data.get("handoff_id"), 3):
        errors.append("handoff_id must be a substantive string")
    if data.get("skill_context") not in {"rigorous-reviewer", "biological-protocol-reviewer", "cross-skill"}:
        errors.append("skill_context is invalid")
    if "notes" in data and not isinstance(data["notes"], str):
        errors.append("notes must be a string")
    if "extensions" in data:
        errors.extend(validate_extensions(data["extensions"]))
    items = data.get("claim_readout_map")
    if not isinstance(items, list) or not items:
        errors.append("claim_readout_map must be a non-empty array")
        return errors
    for idx, item in enumerate(items):
        path = f"claim_readout_map[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be an object")
            continue
        for field in sorted(ITEM_REQUIRED_FIELDS - set(item)):
            errors.append(f"{path} missing required field `{field}`")
        for field in sorted(set(item) - ITEM_REQUIRED_FIELDS):
            errors.append(f"{path} contains unsupported field `{field}`")
        minimum_lengths = {
            "claim_id": 2,
            "claim_text": 8,
            "readout_id": 2,
            "readout_supports": 8,
            "protocol_step_or_method": 4,
            "qc_gate": 8,
            "failure_mode": 8,
            "manuscript_impact": 8,
        }
        for key, minimum_length in minimum_lengths.items():
            if not substantive(item.get(key), minimum_length):
                errors.append(f"{path}.{key} must be substantive")
        if item.get("evidence_role") not in ALLOWED_ROLES:
            errors.append(f"{path}.evidence_role is invalid")
        if item.get("parameter_authority") not in ALLOWED_AUTHORITY:
            errors.append(f"{path}.parameter_authority is invalid")
        if item.get("revision_action") not in ALLOWED_ACTIONS:
            errors.append(f"{path}.revision_action is invalid")
        errors.extend(validate_unique_ids(item.get("source_ids"), f"{path}.source_ids"))
        if item.get("evidence_role") == "decisive":
            if (
                item.get("parameter_authority") in {"recommended_unvalidated", "unresolved"}
                and item.get("revision_action")
                not in {"add_validation", "add_qc_gate", "narrow_claim", "author_input_needed"}
            ):
                errors.append(
                    f"{path}: decisive unresolved/unvalidated readout needs validation, QC, "
                    "claim narrowing, or author input"
                )
            if "control" not in str(item.get("qc_gate", "")).lower() and "对照" not in str(item.get("qc_gate", "")):
                errors.append(f"{path}: decisive readout qc_gate should name control logic")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        data = load_json(args.handoff)
    except Exception as exc:
        print(f"Invalid JSON input: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2, ensure_ascii=False))
    elif errors:
        print("Claim-readout handoff validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Claim-readout handoff validation passed.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
