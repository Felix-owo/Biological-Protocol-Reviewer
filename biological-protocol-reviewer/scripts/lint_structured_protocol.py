#!/usr/bin/env python3
"""Validate structured biological-protocol-reviewer JSON outputs.

This intentionally implements only the JSON Schema subset used by this skill,
so CI can run with the Python standard library and no network dependency.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"
DEFAULT_SCHEMA = SCHEMA_DIR / "review_report.schema.json"
READINESS_RANGES = {
    0: (0.0, 3.9),
    1: (4.0, 5.9),
    2: (6.0, 7.9),
    3: (8.0, 10.0),
}
PROFILE_SECTION_FLAGS = {
    "protocol_panel_applicable": "protocol_panel_synthesis",
    "operator_burden_applicable": "operator_burden_budget",
    "mini_pilot_applicable": "mini_pilot_plan",
    "review_to_sop_mapping_applicable": "review_to_sop_mapping",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_ref(ref: str, root_schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if ref.startswith("#/"):
        resolved: Any = root_schema
        for token in ref[2:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            if not isinstance(resolved, dict) or token not in resolved:
                raise ValueError(f"unresolved local schema reference: {ref}")
            resolved = resolved[token]
        if not isinstance(resolved, dict):
            raise ValueError(f"local schema reference does not resolve to an object: {ref}")
        return resolved, root_schema
    if "/" in ref or ref.startswith("#"):
        raise ValueError(f"unsupported schema reference: {ref}")
    resolved = load_json(SCHEMA_DIR / ref)
    return resolved, resolved


def type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def validate_schema(
    value: Any,
    schema: dict[str, Any],
    path: str = "$",
    root_schema: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if root_schema is None:
        root_schema = schema

    for child_schema in schema.get("allOf", []):
        errors.extend(validate_schema(value, child_schema, path, root_schema))

    if "if" in schema:
        condition_errors = validate_schema(value, schema["if"], path, root_schema)
        branch = schema.get("then") if not condition_errors else schema.get("else")
        if branch:
            errors.extend(validate_schema(value, branch, path, root_schema))

    if "$ref" in schema:
        schema, root_schema = resolve_ref(schema["$ref"], root_schema)

    expected_type = schema.get("type")
    if expected_type and not type_matches(value, expected_type):
        return [f"{path}: expected {expected_type}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value must be one of {schema['enum']}")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: value must equal {schema['const']!r}")

    if isinstance(value, str):
        if "minLength" in schema and len(value.strip()) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: value does not match pattern {schema['pattern']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value above maximum {schema['maximum']}")

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required field `{key}`")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected field `{key}`")

        for key, child_schema in properties.items():
            if key in value:
                errors.extend(validate_schema(value[key], child_schema, f"{path}.{key}", root_schema))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if schema.get("uniqueItems"):
            encoded_items = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(encoded_items) != len(set(encoded_items)):
                errors.append(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(value):
                errors.extend(validate_schema(item, item_schema, f"{path}[{idx}]", root_schema))

    return errors


def _non_empty_unique_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
        and len(value) == len(set(value))
    )


def validate_review_semantics(output: Any) -> list[str]:
    """Enforce cross-field review/profile contracts that JSON Schema cannot express."""
    if not isinstance(output, dict):
        return []

    errors: list[str] = []
    readiness = output.get("readiness")
    if isinstance(readiness, dict):
        score = readiness.get("score")
        maturity = readiness.get("maturity_level")
        if (
            isinstance(score, (int, float))
            and not isinstance(score, bool)
            and isinstance(maturity, int)
            and not isinstance(maturity, bool)
            and maturity in READINESS_RANGES
        ):
            minimum, maximum = READINESS_RANGES[maturity]
            if not minimum <= score <= maximum:
                errors.append(
                    "$.readiness: score "
                    f"{score:g} is inconsistent with maturity_level {maturity} "
                    f"({minimum:g}-{maximum:g})"
                )

    profile = output.get("runtime_profile")
    profile_contract = output.get("profile_contract")
    if isinstance(profile_contract, dict):
        for flag, field in PROFILE_SECTION_FLAGS.items():
            applicable = profile_contract.get(flag)
            if applicable is True and field not in output:
                errors.append(f"$: profile_contract.{flag}=true requires `{field}`")
            if applicable is False and field in output and profile != "protocol_full":
                errors.append(
                    f"$: `{field}` is present although profile_contract.{flag}=false"
                )

    if profile == "protocol_full" and isinstance(profile_contract, dict):
        for flag in PROFILE_SECTION_FLAGS:
            if profile_contract.get(flag) is not True:
                errors.append(f"$: protocol_full requires profile_contract.{flag}=true")

    if profile == "delta_review":
        trace = output.get("delta_review_trace")
        if not isinstance(trace, dict):
            return errors
        prior_open = trace.get("prior_open_finding_ids")
        resolved = trace.get("resolved_finding_ids")
        new = trace.get("new_finding_ids")
        carried = trace.get("carried_forward_finding_ids")
        if not _non_empty_unique_string_list(prior_open):
            errors.append(
                "$.delta_review_trace.prior_open_finding_ids must be a non-empty unique string array"
            )
        delta_lists = (prior_open, resolved, new, carried)
        if all(
            isinstance(value, list)
            and all(isinstance(item, str) for item in value)
            for value in delta_lists
        ):
            prior_set = set(prior_open)
            resolved_set = set(resolved)
            new_set = set(new)
            carried_set = set(carried)
            if resolved_set & carried_set:
                errors.append(
                    "$.delta_review_trace: resolved_finding_ids and "
                    "carried_forward_finding_ids must be disjoint"
                )
            if prior_set != resolved_set | carried_set:
                errors.append(
                    "$.delta_review_trace: prior_open_finding_ids must equal the union of "
                    "resolved_finding_ids and carried_forward_finding_ids"
                )
            if new_set & prior_set:
                errors.append(
                    "$.delta_review_trace: new_finding_ids must not reuse prior open finding IDs"
                )

    return errors


def validate_output(output: Any, schema: dict[str, Any]) -> list[str]:
    errors = validate_schema(output, schema)
    if schema.get("$id") == "review_report.schema.json":
        errors.extend(validate_review_semantics(output))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_output", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        output = load_json(args.json_output)
        schema = load_json(args.schema)
    except Exception as exc:
        print(f"Invalid JSON input or schema: {exc}", file=sys.stderr)
        return 2

    errors = validate_output(output, schema)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2, ensure_ascii=False))
    elif errors:
        print("Structured protocol validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Structured protocol validation passed.")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
