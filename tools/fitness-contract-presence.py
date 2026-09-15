#!/usr/bin/env python3
"""R9/R10/C7/C8 v1: public entrypoints have schema files.

Not a semantic contract checker. V1 only proves files exist and parse.

Goals: a directory under goals/ that contains implementation.py (or *.py)
must contain input.schema.json and output.schema.json (JSON objects).

Nouns: a directory under domain/<noun>/ that contains a *.py module
(not tests/) must contain schemas/verbs.schema.json. That file must parse
as JSON and declare at least one verb with `input` and `output` keys
(either top-level or under a `verbs` object).

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> <kind>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}


def is_skipped_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def goal_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    for base in [root / "goals", *sorted((root / "examples").rglob("goals")) if (root / "examples").is_dir() else []]:
        if not base.is_dir() or is_skipped_dir(base):
            continue
        for child in sorted(base.iterdir()):
            if child.is_dir() and not is_skipped_dir(child):
                found.append(child)
    # also when scan_root is an example tree
    goals = root / "goals"
    if goals.is_dir():
        for child in sorted(goals.iterdir()):
            if child.is_dir() and not is_skipped_dir(child) and child not in found:
                found.append(child)
    return sorted(set(found))


def noun_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    domain = root / "domain"
    if domain.is_dir():
        found.extend(sorted(p for p in domain.iterdir() if p.is_dir()))
    examples = root / "examples"
    if examples.is_dir():
        for domain_dir in sorted(examples.rglob("domain")):
            if domain_dir.is_dir() and domain_dir.name == "domain" and not is_skipped_dir(domain_dir):
                found.extend(sorted(p for p in domain_dir.iterdir() if p.is_dir()))
    return sorted(set(found))


def has_py(dir_path: Path) -> bool:
    for p in dir_path.glob("*.py"):
        if p.is_file():
            return True
    return False


def load_json(path: Path):
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def noun_schema_ok(data: dict) -> bool:
    verbs = data.get("verbs") if isinstance(data.get("verbs"), dict) else data
    if not isinstance(verbs, dict) or not verbs:
        return False
    # skip json-schema metadata keys
    skip = {"$schema", "$id", "$defs", "title", "description", "type", "properties"}
    candidates = verbs.get("properties") if isinstance(verbs.get("properties"), dict) else verbs
    found = False
    for key, spec in candidates.items():
        if key in skip or not isinstance(spec, dict):
            continue
        if "input" in spec and "output" in spec:
            found = True
        elif isinstance(spec.get("properties"), dict):
            props = spec["properties"]
            if "input" in props and "output" in props:
                found = True
    return found


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    violations: list[tuple[str, str]] = []
    for goal in goal_dirs(scan_root):
        if not has_py(goal):
            continue
        for name, kind in (("input.schema.json", "missing-goal-input"), ("output.schema.json", "missing-goal-output")):
            path = goal / name
            if not path.is_file() or load_json(path) is None:
                violations.append((rel(path if path.parent.exists() else goal / name), kind))
    for noun in noun_dirs(scan_root):
        py_files = [p for p in noun.glob("*.py") if p.is_file()]
        if not py_files:
            continue
        schema = noun / "schemas" / "verbs.schema.json"
        data = load_json(schema) if schema.is_file() else None
        if data is None or not noun_schema_ok(data):
            violations.append((rel(schema), "missing-noun-verbs-schema"))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, str]] = set()
    printed = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, kind = item
            print(f"VIOLATION {path} {kind}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
