#!/usr/bin/env python3
"""C23 v2: open findings in FINDINGS.md *or* confirmer FAIL lines.

FINDINGS.md: `- [ ]` / `OPEN:` without rebut/accepted/hole on the line.
CONFIRM.md / PROPOSAL.md: `- C12 — FAIL` without rebut/accepted/hole.

The format legend `PASS|FAIL|N/A` is not a finding.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path>:<line> open-finding
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
OPEN = re.compile(r"^\s*(-\s*\[\s*\]|OPEN:)", re.I)
FAIL = re.compile(r"^\s*[-*]\s*C\d+\s*—\s*FAIL\b")
REBUT = re.compile(r"rebut|accepted|hole|wontfix|won't fix", re.I)
NOTES = ("CONFIRM.md", "PROPOSAL.md")


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def findings_files(root: Path) -> list[Path]:
    return [
        p for p in root.rglob("FINDINGS.md")
        if p.is_file() and not is_skipped(p)
    ]


def note_files(root: Path) -> list[Path]:
    found = []
    for name in NOTES:
        path = root / name
        if path.is_file():
            found.append(path)
    return found


def scan_one(scan_root: Path) -> list[tuple[str, int]]:
    violations = []
    for path in findings_files(scan_root):
        for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if OPEN.match(line) and REBUT.search(line) is None:
                violations.append((rel(path), lineno))
    for path in note_files(scan_root):
        for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if FAIL.match(line) and REBUT.search(line) is None:
                violations.append((rel(path), lineno))
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
            path, lineno = item
            print(f"VIOLATION {path}:{lineno} open-finding")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
