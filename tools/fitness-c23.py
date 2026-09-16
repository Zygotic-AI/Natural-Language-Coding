#!/usr/bin/env python3
"""C23 v1: FINDINGS.md open items must be closed or rebutted.

Looks for FINDINGS.md (any depth under the scan root). Lines matching
`- [ ]` or `OPEN:` without rebut/accepted/hole on the same line fail.

No FINDINGS.md → skip (MET). That is not proof a review ran.

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
REBUT = re.compile(r"rebut|accepted|hole|wontfix|won't fix", re.I)


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


def scan_one(scan_root: Path) -> list[tuple[str, int]]:
    files = findings_files(scan_root)
    if not files:
        return []
    violations = []
    for path in files:
        for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if OPEN.match(line) and REBUT.search(line) is None:
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
