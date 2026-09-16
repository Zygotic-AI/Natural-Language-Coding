#!/usr/bin/env python3
"""C2 v1: adjectives.txt / fields.txt do not live under goals/.

Does not check the noun named in C1. Home = domain/<noun>/, not a goal folder.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> adjectives-in-goal
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
BANNED = {"adjectives.txt", "fields.txt"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def goal_trees(root: Path) -> list[Path]:
    found: list[Path] = []
    direct = root / "goals"
    if direct.is_dir():
        found.append(direct)
    examples = root / "examples"
    if examples.is_dir():
        for p in examples.rglob("goals"):
            if p.is_dir() and p.name == "goals" and not is_skipped(p):
                found.append(p)
    return found


def scan_one(scan_root: Path) -> list[str]:
    hits = []
    for goals in goal_trees(scan_root):
        for path in goals.rglob("*"):
            if not path.is_file() or is_skipped(path):
                continue
            if path.name in BANNED:
                hits.append(rel(path))
    return hits


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
            print(f"VIOLATION {path} adjectives-in-goal")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
