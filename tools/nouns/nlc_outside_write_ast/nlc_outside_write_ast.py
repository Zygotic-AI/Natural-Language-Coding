"""AST helpers for Gate 1 / R33 bypass detection (O9a)."""

from __future__ import annotations

import ast
from typing import Iterable


def _field_from_constant(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def ast_field_write_violations(source: str, fields: set[str]) -> list[tuple[int, str]]:
    """Detect noun field writes that bypass line-regex Gate 1 checks."""
    if not fields:
        return []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    hits: list[tuple[int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "__setattr__":
                if isinstance(func.value, ast.Name) and func.value.id == "object":
                    if len(node.args) >= 2:
                        field = _field_from_constant(node.args[1])
                        if field and field in fields:
                            hits.append((node.lineno, field))
            if isinstance(func, ast.Name) and func.id == "setattr" and len(node.args) >= 2:
                field = _field_from_constant(node.args[1])
                if field and field in fields:
                    hits.append((node.lineno, field))
        if isinstance(node, ast.Assign):
            for target in node.targets:
                hits.extend(_assign_targets(target, node.lineno, fields))
    return hits


def _assign_targets(target: ast.AST, lineno: int, fields: set[str]) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    if isinstance(target, ast.Subscript):
        key = _field_from_constant(target.slice) if isinstance(target.slice, ast.Constant) else None
        if not key and isinstance(target.slice, ast.Constant):
            key = _field_from_constant(target.slice)
        val = target.value
        if isinstance(val, ast.Attribute) and val.attr == "__dict__" and key and key in fields:
            out.append((lineno, key))
        if isinstance(val, ast.Call) and isinstance(val.func, ast.Name) and val.func.id == "vars":
            if key and key in fields:
                out.append((lineno, key))
    if isinstance(target, ast.Attribute) and isinstance(target.attr, str) and target.attr in fields:
        out.append((lineno, target.attr))
    return out


def ast_escape_hatch_violations(source: str) -> list[tuple[int, str]]:
    """Detect R33 reflection / setattr / dict hatches via AST."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    hits: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                if func.id in {"setattr", "vars", "exec", "eval"}:
                    hits.append((node.lineno, f"{func.id}-hatch"))
            if isinstance(func, ast.Attribute) and func.attr == "__setattr__":
                if isinstance(func.value, ast.Name) and func.value.id == "object":
                    hits.append((node.lineno, "object-setattr-hatch"))
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Attribute):
                    if target.value.attr == "__dict__":
                        hits.append((node.lineno, "dict-hatch"))
    return hits
