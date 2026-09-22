#!/usr/bin/env python3
"""ADR 0007/0009: gaps documented — no fake binders claiming MET."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENFORCEMENT = ROOT / "docs" / "ADR-ENFORCEMENT.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not ENFORCEMENT.is_file():
        violations.append("missing ADR-ENFORCEMENT.md")
    else:
        text = ENFORCEMENT.read_text(encoding="utf-8", errors="replace")
        if "| 0007 |" not in text or "gap" not in text.split("| 0007 |", 1)[1][:80].lower():
            violations.append("ADR-ENFORCEMENT must mark 0007 as gap")
        if "| 0009 |" not in text or "gap" not in text.split("| 0009 |", 1)[1][:80].lower():
            violations.append("ADR-ENFORCEMENT must mark 0009 as gap")
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
