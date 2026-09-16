#!/usr/bin/env python3
"""C24 v1: classes that require ratification record it in the note.

If PROPOSAL.md / CONFIRM.md states change class A, B, D, E, or F, the same
file must mention ratify/ratification. Class C → skip.

No note → skip (MET).

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> missing-ratification
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ("PROPOSAL.md", "CONFIRM.md")
CLASS = re.compile(r"change\s*class\s*[:*\s]*([ABDEF])\b", re.I)
RATIFY = re.compile(r"\bratify|\bratification\b", re.I)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scan_one(scan_root: Path) -> list[str]:
    missing = []
    for name in NOTES:
        path = scan_root / name
        if not path.is_file():
            continue
        text = path.read_text(errors="replace")
        if CLASS.search(text) is None:
            continue
        if RATIFY.search(text) is None:
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
            print(f"VIOLATION {path} missing-ratification")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
