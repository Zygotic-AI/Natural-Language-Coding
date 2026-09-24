#!/usr/bin/env python3
"""P4 / R31 v1 for code boundaries: failure mode declared.


R9 already requires input.schema.json + output.schema.json.
This tool only runs where those two exist. Then failure.schema.json
(or error.schema.json) must exist and parse, and each verb in
schemas/verbs.schema.json that has input+output must also have
error or failure.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> <kind>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def collect_named_children(root: Path, folder: str) -> list[Path]:
    found: list[Path] = []
    direct = root / folder
    if direct.is_dir():
        found.extend(p for p in direct.iterdir() if p.is_dir() and not is_skipped(p))
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob(folder):
            if named.is_dir() and named.name == folder and not is_skipped(named):
                found.extend(p for p in named.iterdir() if p.is_dir() and not is_skipped(p))
    return sorted(set(found))


def load_json(path: Path):
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def verb_map(data: dict) -> dict:
    if isinstance(data.get("verbs"), dict):
        return data["verbs"]
    return data


def has_failure(spec: dict) -> bool:
    if "error" in spec or "failure" in spec:
        return True
    props = spec.get("properties")
    return isinstance(props, dict) and ("error" in props or "failure" in props)


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    violations: list[tuple[str, str]] = []
    for goal in collect_named_children(scan_root, "goals"):
        inp = goal / "input.schema.json"
        out = goal / "output.schema.json"
        if not inp.is_file() or not out.is_file():
            continue
        fail = goal / "failure.schema.json"
        err = goal / "error.schema.json"
        chosen = fail if fail.is_file() else err
        if not chosen.is_file() or load_json(chosen) is None:
            violations.append((rel(fail), "missing-goal-failure"))
    for noun in collect_named_children(scan_root, "domain"):
        schema = noun / "schemas" / "verbs.schema.json"
        data = load_json(schema) if schema.is_file() else None
        if data is None:
            continue
        verbs = verb_map(data)
        skip = {"$schema", "$id", "$defs", "title", "description", "type", "properties", "verbs"}
        for name, spec in verbs.items():
            if name in skip or not isinstance(spec, dict):
                continue
            if "input" in spec and "output" in spec and not has_failure(spec):
                violations.append((rel(schema) + "#" + name, "missing-verb-failure"))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen = set()
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
