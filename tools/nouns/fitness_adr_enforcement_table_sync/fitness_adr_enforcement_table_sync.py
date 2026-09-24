#!/usr/bin/env python3
"""ADR-ENFORCEMENT gap rows must not contradict FINDINGS done/bound (F3)."""

from __future__ import annotations



import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ENFORCEMENT = ROOT / "docs" / "ADR-ENFORCEMENT.md"
FINDINGS = ROOT / "FINDINGS.md"

# ADRs closed in FINDINGS but still `gap` in enforcement (expand as needed).
CLOSED_MARKERS: dict[str, list[re.Pattern[str]]] = {
    "0029": [
        re.compile(r"park-0029.*@done", re.I),
        re.compile(r"ADR\s+0029\s*\|[^|]*\*\*Closed\*\*", re.I),
        re.compile(r"0029 lineage tools.*\bdone\b", re.I),
    ],
}


def main() -> int:
    _ = sys.argv[1:]
    if not ENFORCEMENT.is_file() or not FINDINGS.is_file():
        print("VIOLATION missing ADR-ENFORCEMENT or FINDINGS")
        print("RESULT:NOT_MET")
        return 1

    enf = ENFORCEMENT.read_text(encoding="utf-8", errors="replace")
    find = FINDINGS.read_text(encoding="utf-8", errors="replace")
    violations: list[str] = []

    for adr, patterns in CLOSED_MARKERS.items():
        row_gap = re.search(
            rf"\|\s*{adr}\s*\|[^\n]*\|\s*(?:\*\*gap\*\*|gap)\s*\|",
            enf,
            re.I,
        )
        if not row_gap:
            continue
        if any(p.search(find) for p in patterns):
            violations.append(f"ADR {adr}: ENFORCEMENT still gap but FINDINGS marks closed")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

