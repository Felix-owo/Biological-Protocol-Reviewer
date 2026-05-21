#!/usr/bin/env python3
"""Validate structured Biological-Protocol-Reviewer JSON outputs.

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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_ref(ref: str) -> dict[str, Any]:
    if "/" in ref or ref.startswith("#"):
        raise ValueError(f"unsupported schema reference: {ref}")
    return load_json(SCHEMA_DIR / ref)


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


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []

    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"])

    expected_type = schema.get("type")
    if expected_type and not type_matches(value, expected_type):
        return [f"{path}: expected {expected_type}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value must be one of {schema['enum']}")

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
                errors.extend(validate_schema(value[key], child_schema, f"{path}.{key}"))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(value):
                errors.extend(validate_schema(item, item_schema, f"{path}[{idx}]"))

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

    errors = validate_schema(output, schema)
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
