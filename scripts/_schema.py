"""Minimal, dependency-free JSON Schema subset validator.

CI runs with only the Python standard library, so this supports exactly the
keywords our schemas use: type, required, properties, additionalProperties
(false), enum, pattern, minLength, minItems, items. Unknown keywords are
ignored; this is not a general JSON Schema implementation.
"""
from __future__ import annotations

import re
from typing import Any

_TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "integer": int, "number": (int, float),
}


def validate(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    if "enum" in schema and value not in schema["enum"]:
        return [f"{path}: {value!r} not one of {schema['enum']}"]
    expected = schema.get("type")
    if expected:
        py_type = _TYPES[expected]
        # bool is a subclass of int; don't let True pass as an integer/number.
        if not isinstance(value, py_type) or (expected in {"integer", "number"} and isinstance(value, bool)):
            return [f"{path}: expected {expected}, got {type(value).__name__}"]
    errors: list[str] = []
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: needs at least {schema['minItems']} item(s)")
        if "items" in schema:
            for i, item in enumerate(value):
                errors.extend(validate(item, schema["items"], f"{path}[{i}]"))
    if isinstance(value, dict):
        props = schema.get("properties", {})
        errors.extend(f"{path}: missing required {key!r}" for key in schema.get("required", [])
                      if key not in value)
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}: unexpected key {key!r}" for key in value if key not in props)
        for key, sub in props.items():
            if key in value:
                errors.extend(validate(value[key], sub, f"{path}.{key}"))
    return errors
