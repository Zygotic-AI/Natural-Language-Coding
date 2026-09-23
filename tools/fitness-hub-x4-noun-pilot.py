#!/usr/bin/env python3
"""X4 noun pilots: every tools/nouns/<slug>/ package has shape + CLI adapter import."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOUNS = ROOT / "tools" / "nouns"
REMAINDER = ROOT / "integrity" / "hub-x4-remainder.json"


def pilots_from_ssot() -> list[dict]:
    data = json.loads(REMAINDER.read_text(encoding="utf-8"))
    return list(data.get("noun_pilots") or [])


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    pilots = pilots_from_ssot()
    if len(pilots) < 2:
        violations.append("hub-x4-remainder.json noun_pilots must list X4 noun packages")
    for pilot in pilots:
        noun_dir = ROOT / pilot["path"]
        if not noun_dir.is_dir():
            violations.append(f"missing noun dir {pilot['path']}")
            continue
        py_files = [p for p in noun_dir.glob("*.py") if p.name != "__init__.py"]
        if not py_files:
            violations.append(f"{pilot['path']} missing implementation .py")
            continue
        mod = py_files[0]
        try:
            tree = ast.parse(mod.read_text(encoding="utf-8"), filename=str(mod))
        except SyntaxError as exc:
            violations.append(f"{mod.relative_to(ROOT)} syntax: {exc}")
            continue
        has_boundary = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if (
                        isinstance(t, ast.Name)
                        and t.id == "BOUNDARY"
                        and isinstance(node.value, ast.Constant)
                        and node.value.value == "bba-emit"
                    ):
                        has_boundary = True
        if not has_boundary:
            violations.append(f"{mod.relative_to(ROOT)} lacks BOUNDARY = \"bba-emit\"")
        for extra in ("README.md", "adjectives.txt", "fields.txt", "schemas/verbs.schema.json"):
            if not (noun_dir / extra).is_file():
                violations.append(f"missing {pilot['path']}{extra}")
        hint = f"nouns.{Path(pilot['path'].rstrip('/')).name}"
        for name in pilot.get("adapters") or []:
            path = ROOT / "tools" / name
            if not path.is_file():
                violations.append(f"missing adapter {name}")
                continue
            text = path.read_text(encoding="utf-8")
            if hint not in text and f"nouns.{pilot.get('noun')}" not in text:
                violations.append(f"{name} must import {hint}")
    # emit_path_open must be empty when complete flag set
    data = json.loads(REMAINDER.read_text(encoding="utf-8"))
    if data.get("emit_path_complete") and data.get("emit_path_open"):
        violations.append("emit_path_complete but emit_path_open non-empty")
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print(f"RESULT:MET pilots={len(pilots)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
