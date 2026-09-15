#!/usr/bin/env python3
"""R11 / C9 v1: same field name, different JSON type, fails.

Walks *.schema.json under the scan root. Records each `properties.<name>.type`.
If one name is used with two different types in the tree, that is a fork.

Does not prove two names mean the same thing (balance vs remaining). V1 is
name+type only.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <name> types=<a,b> <path> ...
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def schema_files(root: Path) -> list[Path]:
    out = []
    if not root.is_dir():
        return out
    for path in root.rglob("*.schema.json"):
        if path.is_file() and not is_skipped(path):
            out.append(path)
    return sorted(out)


def walk_properties(node, found: list[tuple[str, str]]) -> None:
    if isinstance(node, list):
        for item in node:
            walk_properties(item, found)
        return
    if not isinstance(node, dict):
        return
    props = node.get("properties")
    if isinstance(props, dict):
        for name, spec in props.items():
            if isinstance(spec, dict) and isinstance(spec.get("type"), str):
                found.append((name, spec["type"]))
            walk_properties(spec, found)
    for key, val in node.items():
        if key == "properties":
            continue
        walk_properties(val, found)


def scan_one(scan_root: Path) -> list[tuple[str, list[str], list[str]]]:
    uses: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for path in schema_files(scan_root):
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        found: list[tuple[str, str]] = []
        walk_properties(data, found)
        for name, typ in found:
            uses[name][typ].add(rel(path))
    violations = []
    for name, type_map in sorted(uses.items()):
        if len(type_map) < 2:
            continue
        types = sorted(type_map)
        paths = sorted({p for s in type_map.values() for p in s})
        violations.append((name, types, paths))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    printed = []
    seen = set()
    for scan_root in scan_roots:
        for name, types, paths in scan_one(scan_root):
            key = (name, tuple(types), tuple(paths))
            if key in seen:
                continue
            seen.add(key)
            printed.append(key)
            print(f"VIOLATION {name} types={','.join(types)} " + " ".join(paths))
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
