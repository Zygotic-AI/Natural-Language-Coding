#!/usr/bin/env python3
"""C1 v1: if a proposal/confirm note exists, it states change class A–F.

No note file → skip (MET). That is not proof the change was classified.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> missing-change-class
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ("PROPOSAL.md", "CONFIRM.md")
CLASS = re.compile(r"change\s*class\s*[:*\s]*[A-F]\b", re.I)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def note_files(scan_root: Path) -> list[Path]:
    return [scan_root / n for n in NOTES if (scan_root / n).is_file()]


def scan_one(scan_root: Path) -> list[str]:
    notes = note_files(scan_root)
    if not notes:
        return []
    missing = []
    for path in notes:
        text = path.read_text(errors="replace")
        if CLASS.search(text) is None:
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
            print(f"VIOLATION {path} missing-change-class")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
