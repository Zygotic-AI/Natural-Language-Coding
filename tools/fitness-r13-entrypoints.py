#!/usr/bin/env python3
"""R13 v1: one public entrypoint file per goal directory.

Counts files whose stem is implementation|run|main|index|handler|entry|public
inside goals/<id>/. Two or more is a second door.

Does not parse exports. C11 stays unbound (diff-scoped).

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <goal> extra-entrypoint <file> ...
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EXTS = {".ts", ".js", ".py", ".mjs", ".cjs", ".tsx", ".jsx"}
ENTRY_STEMS = {"implementation", "run", "main", "index", "handler", "entry", "public"}
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def goal_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    goals = root / "goals"
    if goals.is_dir():
        found.extend(p for p in goals.iterdir() if p.is_dir())
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob("goals"):
            if named.is_dir() and named.name == "goals" and not is_skipped(named):
                found.extend(p for p in named.iterdir() if p.is_dir())
    return sorted(set(found))


def scan_one(scan_root: Path) -> list[tuple[str, list[str]]]:
    violations = []
    for goal in goal_dirs(scan_root):
        entries = sorted(
            p.name
            for p in goal.iterdir()
            if p.is_file() and p.suffix in SOURCE_EXTS and p.stem in ENTRY_STEMS
        )
        if len(entries) > 1:
            violations.append((rel(goal), entries))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, tuple[str, ...]]] = set()
    printed: list[tuple[str, list[str]]] = []
    for scan_root in scan_roots:
        for goal, entries in scan_one(scan_root):
            key = (goal, tuple(entries))
            if key in seen:
                continue
            seen.add(key)
            printed.append((goal, entries))
            print(f"VIOLATION {goal} extra-entrypoint " + " ".join(entries))
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
