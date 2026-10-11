#!/usr/bin/env python3
"""Refuse root-level agent session artifacts (O5 / v0.3.0 stabilization).

Input: no argv. Scans repository root only.

Output: VIOLATION lines, then RESULT:MET or RESULT:NOT_MET.

Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# Names that must never appear as root-level session/chat dumps.
FORBIDDEN_ROOT_NAMES = frozenset({"in-process", "agent"})


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for name in sorted(FORBIDDEN_ROOT_NAMES):
        path = ROOT / name
        if path.exists():
            violations.append(f"root session artifact present: {name}")
    if (ROOT / ".gitignore").is_file():
        text = (ROOT / ".gitignore").read_text(encoding="utf-8", errors="replace")
        for name in FORBIDDEN_ROOT_NAMES:
            if f"/{name}" not in text and name not in text.splitlines():
                violations.append(f".gitignore must refuse /{name}")
    else:
        violations.append("missing root .gitignore")

    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
