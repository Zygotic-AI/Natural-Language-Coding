#!/usr/bin/env python3
"""ADR 0023/UC15: ./nlc adopt-existing points at goal-scaffold + RULE-TRACE."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    text = read_tool("tools/nlc.py")
    violations: list[str] = []
    if "cmd_adopt_existing" not in text:
        violations.append("nlc.py missing cmd_adopt_existing")
    if "goal-scaffold" not in text or "RULE-TRACE" not in text:
        violations.append("cmd_adopt_existing must print goal-scaffold and RULE-TRACE hints")
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

