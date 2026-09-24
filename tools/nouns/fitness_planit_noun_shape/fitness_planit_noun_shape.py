#!/usr/bin/env python3
"""ADR 0008: planit generate step cites noun-inheritance fitness."""

from __future__ import annotations



import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLANIT = ROOT / ".agents" / "skills" / "planit" / "SKILL.md"


def main() -> int:
    _ = sys.argv[1:]
    if not PLANIT.is_file():
        print("VIOLATION missing planit SKILL")
        print("RESULT:NOT_MET")
        return 1
    text = PLANIT.read_text(encoding="utf-8", errors="replace")
    if "fitness-no-noun-inheritance" not in text:
        print("VIOLATION planit must cite fitness-no-noun-inheritance.py on domain generate")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

