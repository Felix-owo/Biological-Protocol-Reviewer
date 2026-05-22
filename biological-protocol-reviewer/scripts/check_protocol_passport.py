#!/usr/bin/env python3
"""Validate a biological-protocol-reviewer Protocol Passport.

Accepts JSON directly. For YAML, this supports the simple YAML subset used by
templates/protocol_passport_template.yaml and falls back to structural text
checks if PyYAML is unavailable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_KEYS = [
    "protocol_id",
    "skill_version",
    "source_materials",
    "sample_material",
    "primary_readout",
    "experimental_unit",
    "module_activation",
    "parameter_authority",
    "qc_gates",
    "local_validation_status",
    "safety_governance_status",
    "unresolved_gaps",
    "mini_pilot_plan",
    "review_to_sop_mapping",
    "validator_status",
]
AUTHORITY_CLASSES = {
    "Original protocol fact",
    "Local validated parameter",
    "External benchmark",
    "Vendor/manual standard",
    "Institutional/core-facility SOP",
    "Recommended but unvalidated",
    "Unresolved gap",
    "Companion-derived lead",
}


def load_data(path: Path) -> tuple[Any, list[str]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text), []
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text), []
    except Exception:
        missing = [key for key in REQUIRED_KEYS if not re.search(rf"^{re.escape(key)}\s*:", text, re.M)]
        return {"__raw_yaml_text__": text}, [f"YAML parser unavailable; missing top-level key `{key}`" for key in missing]


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: Any, parser_warnings: list[str]) -> tuple[list[str], list[str]]:
    errors = list(parser_warnings)
    warnings: list[str] = []

    if "__raw_yaml_text__" in data:
        return errors, ["Only top-level YAML keys were checked because PyYAML is unavailable."]

    if not isinstance(data, dict):
        return ["passport must be an object"], warnings

    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing required field `{key}`")

    if not non_empty_string(data.get("skill_version")):
        errors.append("skill_version must be non-empty")
    if not non_empty_string(data.get("primary_readout")):
        errors.append("primary_readout must be non-empty")
    if not non_empty_string(data.get("experimental_unit")):
        errors.append("experimental_unit must be non-empty")

    module_activation = data.get("module_activation")
    if not isinstance(module_activation, dict):
        errors.append("module_activation must be an object")
    else:
        for key in ["activated", "unclear", "not_applicable"]:
            if not isinstance(module_activation.get(key), list):
                errors.append(f"module_activation.{key} must be an array")

    parameter_authority = data.get("parameter_authority")
    if not isinstance(parameter_authority, list) or not parameter_authority:
        errors.append("parameter_authority must be a non-empty array")
    else:
        for idx, item in enumerate(parameter_authority):
            path = f"parameter_authority[{idx}]"
            if not isinstance(item, dict):
                errors.append(f"{path} must be an object")
                continue
            for key in ["parameter", "authority_class", "local_validation_status"]:
                if not non_empty_string(item.get(key)):
                    errors.append(f"{path}.{key} must be non-empty")
            authority_class = item.get("authority_class")
            if authority_class and authority_class not in AUTHORITY_CLASSES:
                warnings.append(f"{path}.authority_class is non-standard: {authority_class}")
            if authority_class in {"Recommended but unvalidated", "Unresolved gap"}:
                label = str(item.get("sop_label", ""))
                if "TO BE VERIFIED LOCALLY" not in label and "TO BE CONFIRMED" not in label:
                    errors.append(f"{path}.sop_label must preserve verification/confirmation status")

    qc_gates = data.get("qc_gates")
    if not isinstance(qc_gates, list) or not qc_gates:
        errors.append("qc_gates must be a non-empty array")
    else:
        for idx, gate in enumerate(qc_gates):
            path = f"qc_gates[{idx}]"
            if not isinstance(gate, dict):
                errors.append(f"{path} must be an object")
                continue
            for key in ["gate_id", "readout_id", "acceptance_criterion", "fail_action"]:
                if not non_empty_string(gate.get(key)):
                    errors.append(f"{path}.{key} must be non-empty")

    mini_pilot = data.get("mini_pilot_plan")
    if not isinstance(mini_pilot, dict):
        errors.append("mini_pilot_plan must be an object")
    elif not isinstance(mini_pilot.get("required"), bool):
        errors.append("mini_pilot_plan.required must be boolean")

    mapping = data.get("review_to_sop_mapping")
    if not isinstance(mapping, list) or not mapping:
        errors.append("review_to_sop_mapping must be a non-empty array")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("passport", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        data, parser_warnings = load_data(args.passport)
    except Exception as exc:
        print(f"Invalid passport input: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(data, parser_warnings)
    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Protocol passport validation passed." if result["ok"] else "Protocol passport validation failed:")
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        for warning in warnings:
            print(f"WARN: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
