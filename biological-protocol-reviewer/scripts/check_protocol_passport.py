#!/usr/bin/env python3
"""Validate a biological-protocol-reviewer Protocol Passport.

Accepts JSON directly and uses PyYAML for completed YAML passports. Use
``--allow-template`` only for the bundled blank template. If PyYAML is
unavailable, template mode accepts only content byte-for-byte identical to that
bundled template; every other YAML artifact fails closed.
"""

from __future__ import annotations

import argparse
import json
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
BUNDLED_TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "protocol_passport_template.yaml"


def raw_template_structure(path: Path, text: str) -> tuple[Any, list[str]]:
    try:
        bundled_bytes = BUNDLED_TEMPLATE.read_bytes()
        candidate_bytes = path.read_bytes()
    except OSError as exc:
        return {"__raw_yaml_text__": text}, [f"bundled passport template is unavailable: {exc}"]
    if candidate_bytes != bundled_bytes:
        return {"__raw_yaml_text__": text}, [
            "PyYAML is unavailable; --allow-template accepts only content exactly "
            "matching the bundled protocol_passport_template.yaml"
        ]
    return {"__raw_yaml_text__": text}, []


def load_data(path: Path, allow_template: bool = False) -> tuple[Any, list[str]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text), []
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError as exc:
        if exc.name != "yaml":
            raise
        if allow_template:
            return raw_template_structure(path, text)
        return {"__raw_yaml_text__": text}, [
            "PyYAML is required for completed YAML passport validation; "
            "install PyYAML or provide JSON"
        ]
    try:
        return yaml.safe_load(text), []
    except Exception as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc


def non_empty_string(
    value: Any,
    allow_empty_placeholder: bool = False,
    min_length: int = 1,
) -> bool:
    if allow_empty_placeholder and value == "":
        return True
    return isinstance(value, str) and len(value.strip()) >= min_length


def _require_string(
    item: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    allow_empty_template: bool,
    min_length: int = 1,
) -> None:
    if not non_empty_string(item.get(key), allow_empty_template, min_length):
        errors.append(f"{path}.{key} must contain at least {min_length} characters")


def validate(
    data: Any,
    parser_warnings: list[str],
    allow_empty_template: bool = False,
) -> tuple[list[str], list[str]]:
    errors = list(parser_warnings)
    warnings: list[str] = []

    if isinstance(data, dict) and "__raw_yaml_text__" in data:
        if allow_empty_template and not errors:
            return [], ["Bundled YAML template identity was verified without PyYAML."]
        return errors, ["Completed YAML content was not parsed because PyYAML is unavailable."]

    if not isinstance(data, dict):
        return ["passport must be an object"], warnings

    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing required field `{key}`")

    for key, minimum in {
        "protocol_id": 3,
        "skill_version": 8,
        "primary_readout": 4,
        "experimental_unit": 4,
        "local_validation_status": 4,
    }.items():
        if not non_empty_string(data.get(key), allow_empty_template, minimum):
            errors.append(f"{key} must contain at least {minimum} characters")

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
            for key, minimum in {
                "parameter": 2,
                "authority_class": 4,
                "source_identity": 2,
                "local_validation_status": 4,
            }.items():
                _require_string(item, key, path, errors, allow_empty_template, minimum)
            for key in ["value", "sop_label"]:
                if key not in item or not isinstance(item.get(key), str):
                    errors.append(f"{path}.{key} must be a string")
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
            for key, minimum in {
                "gate_id": 1,
                "readout_id": 1,
                "acceptance_criterion": 4,
                "fail_action": 4,
            }.items():
                _require_string(gate, key, path, errors, allow_empty_template, minimum)

    mini_pilot = data.get("mini_pilot_plan")
    if not isinstance(mini_pilot, dict):
        errors.append("mini_pilot_plan must be an object")
    elif not isinstance(mini_pilot.get("required"), bool):
        errors.append("mini_pilot_plan.required must be boolean")
    elif not isinstance(mini_pilot.get("summary"), str):
        errors.append("mini_pilot_plan.summary must be a string")

    mapping = data.get("review_to_sop_mapping")
    if not isinstance(mapping, list) or not mapping:
        errors.append("review_to_sop_mapping must be a non-empty array")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("passport", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--allow-template",
        action="store_true",
        help="Allow blank placeholder strings in the bundled protocol passport template.",
    )
    args = parser.parse_args()

    try:
        data, parser_warnings = load_data(args.passport, allow_template=args.allow_template)
    except Exception as exc:
        print(f"Invalid passport input: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(data, parser_warnings, allow_empty_template=args.allow_template)
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
