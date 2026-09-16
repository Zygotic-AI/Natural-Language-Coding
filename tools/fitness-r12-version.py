#!/usr/bin/env python3
"""R12 v1: public contract JSON has a top-level version.

Not C10 (breaking change + ADR). Presence of `version` as a non-empty
string or number. Does not compare versions across commits.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> missing-version
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


def collect_named_children(root: Path, folder: str) -> list[Path]:
    found: list[Path] = []
    direct = root / folder
    if direct.is_dir():
        found.extend(p for p in direct.iterdir() if p.is_dir() and not is_skipped_dir(p))
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob(folder):
            if named.is_dir() and named.name == folder and not is_skipped_dir(named):
                found.extend(p for p in named.iterdir() if p.is_dir() and not is_skipped_dir(p))
    return sorted(set(found))


def has_py(dir_path: Path) -> bool:
    return any(p.is_file() for p in dir_path.glob("*.py"))


def load_json(path: Path):
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def version_ok(data: dict | None) -> bool:
    if not data:
        return False
    v = data.get("version")
    if isinstance(v, str) and v.strip():
        return True
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return True
    return False


def scan_one(scan_root: Path) -> list[str]:
    missing: list[str] = []
    for goal in collect_named_children(scan_root, "goals"):
        if not has_py(goal):
            continue
        for name in ("input.schema.json", "output.schema.json", "failure.schema.json"):
            path = goal / name
            if not path.is_file():
                continue
            if not version_ok(load_json(path)):
                missing.append(rel(path))
    for noun in collect_named_children(scan_root, "domain"):
        if not has_py(noun):
            continue
        path = noun / "schemas" / "verbs.schema.json"
        if not path.is_file():
            continue
        if not version_ok(load_json(path)):
            missing.append(rel(path))
    return missing


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[str] = set()
    printed: list[str] = []
    for scan_root in scan_roots:
        for path in scan_one(scan_root):
            if path in seen:
                continue
            seen.add(path)
            printed.append(path)
            print(f"VIOLATION {path} missing-version")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
