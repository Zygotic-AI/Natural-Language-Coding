#!/usr/bin/env python3
"""C13 / R16 v1: a one-verb goal with no I/O schemas is a wrapper, not a goal.

If goals/<id>/*.py has exactly one `.verb(` call and neither input.schema.json
nor output.schema.json, fail. Schemas present = I/O; allowed (invoice-correct).

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <goal> wrapper-goal
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}
CALL = re.compile(r"\.[A-Za-z_][A-Za-z0-9_]*\s*\(")


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def goal_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    direct = root / "goals"
    if direct.is_dir():
        found.extend(p for p in direct.iterdir() if p.is_dir() and not is_skipped(p))
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob("goals"):
            if named.is_dir() and named.name == "goals" and not is_skipped(named):
                found.extend(p for p in named.iterdir() if p.is_dir() and not is_skipped(p))
    return found


def call_count(text: str) -> int:
    body = "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("#"))
    return len(CALL.findall(body))


def scan_one(scan_root: Path) -> list[str]:
    violations = []
    for goal in goal_dirs(scan_root):
        py_files = [
            p for p in goal.glob("*.py")
            if p.is_file() and not p.name.startswith("test_")
        ]
        if not py_files:
            continue
        has_io = (goal / "input.schema.json").is_file() or (goal / "output.schema.json").is_file()
        if has_io:
            continue
        total = 0
        for path in py_files:
            total += call_count(path.read_text(errors="replace"))
        if total == 1:
            violations.append(rel(goal))
    return violations


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
            print(f"VIOLATION {path} wrapper-goal")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
