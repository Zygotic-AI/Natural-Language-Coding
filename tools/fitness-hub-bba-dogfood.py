#!/usr/bin/env python3
"""X4 v1: hub emit path creates BBA nouns/ + goals/ homes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDED = (
    ROOT / "templates" / "adopter" / "nouns" / "README.md",
    ROOT / "templates" / "adopter" / "goals" / "README.md",
    ROOT / "docs" / "nlc" / "HUB-BBA-DOGFOOD.md",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in NEEDED:
        if not path.is_file():
            violations.append(f"missing {path.relative_to(ROOT)}")
    init = (ROOT / "tools" / "nlc-init.py").read_text(encoding="utf-8", errors="replace")
    if '(target / "nouns")' not in init:
        violations.append("nlc-init.py does not create nouns/")
    if '(target / "goals")' not in init:
        violations.append("nlc-init.py does not create goals/")
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
