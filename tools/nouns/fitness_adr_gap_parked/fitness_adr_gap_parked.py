#!/usr/bin/env python3
"""ADR 0007/0009/0028: enforcement rows are bound, not left as gaps."""

from __future__ import annotations



import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ENFORCEMENT = ROOT / "docs" / "ADR-ENFORCEMENT.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not ENFORCEMENT.is_file():
        violations.append("missing ADR-ENFORCEMENT.md")
    else:
        text = ENFORCEMENT.read_text(encoding="utf-8", errors="replace")
        for adr in ("0007", "0009", "0028"):
            if f"| {adr} |" not in text:
                violations.append(f"ADR-ENFORCEMENT missing {adr}")
                continue
            cell = text.split(f"| {adr} |", 1)[1].split("\n", 1)[0].lower()
            if "gap" in cell or "bound" not in cell:
                violations.append(f"ADR-ENFORCEMENT must mark {adr} bound and not gap")
    for adr in ("0007", "0009"):
        path = ROOT / "adrs"
        if path.is_dir():
            matches = list(path.glob(f"{adr}-*.md"))
            if not matches:
                violations.append(f"expected adrs/{adr}-*.md")
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

