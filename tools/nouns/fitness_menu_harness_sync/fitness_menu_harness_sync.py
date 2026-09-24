#!/usr/bin/env python3
"""ADR 0017/0020: human menu SSOT matches docs/nlc/MENU.md."""

from __future__ import annotations



import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MENU = ROOT / "docs" / "nlc" / "MENU.md"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_menu_data import SHORT_MAP

    if not MENU.is_file():
        print("VIOLATION missing docs/nlc/MENU.md")
        print("RESULT:NOT_MET")
        return 1
    text = MENU.read_text(encoding="utf-8")
    violations: list[str] = []
    if "nlc_menu_data" not in text:
        violations.append("MENU.md must cite tools/nlc_menu_data.py")
    if "0020" not in text:
        violations.append("MENU.md must cite ADR 0020")
    if "./nlc verify" not in text:
        violations.append("MENU.md must list ./nlc verify for humans")
    if "/planit" not in text:
        violations.append("MENU.md must list /planit for agents")
    if len(SHORT_MAP) < 5:
        violations.append("nlc_menu_data SHORT_MAP too short")
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

