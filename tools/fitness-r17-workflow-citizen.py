#!/usr/bin/env python3
"""R17 v1: workflows/ may host a goal; it may not *be* a goal.

A directory under workflows/ that has implementation.py (or run.py) *and*
input.schema.json is a second citizen. A thin host.py with no goal schemas
is allowed.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <dir> workflow-citizen
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
CODE = {"implementation.py", "run.py", "main.py", "index.py"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def workflow_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    direct = root / "workflows"
    if direct.is_dir():
        found.append(direct)
    examples = root / "examples"
    if examples.is_dir():
        for p in examples.rglob("workflows"):
            if p.is_dir() and p.name == "workflows" and not is_skipped(p):
                found.append(p)
    return found


def scan_one(scan_root: Path) -> list[str]:
    violations = []
    for wf in workflow_dirs(scan_root):
        children = [p for p in wf.iterdir() if p.is_dir() and not is_skipped(p)]
        targets = children if children else [wf]
        for d in targets:
            names = {p.name for p in d.iterdir() if p.is_file()}
            has_code = bool(names & CODE)
            has_contract = "input.schema.json" in names or "output.schema.json" in names
            if has_code and has_contract:
                violations.append(rel(d))
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
            print(f"VIOLATION {path} workflow-citizen")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
