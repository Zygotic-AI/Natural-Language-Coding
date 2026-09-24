#!/usr/bin/env python3
"""ADR 0008: noun-inheritance scan + landmine + planit/reviewer cite."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = read_tool("tools/ci_fitness.py")
    for name in ("fitness-no-noun-inheritance.py", "assert-noun-inheritance-fails.py", "fitness-planit-noun-shape.py"):
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
    if "assert-noun-inheritance" not in ci:
        violations.append("ci_fitness must run assert-noun-inheritance landmine")
    if not (ROOT / "examples/noun-inheritance-violation").is_dir():
        violations.append("missing examples/noun-inheritance-violation")
    reviewer = ROOT / ".agents/skills/bbp-reviewer/SKILL.md"
    if reviewer.is_file() and "fitness-no-noun-inheritance" not in reviewer.read_text(encoding="utf-8", errors="replace"):
        violations.append("bbp-reviewer must cite fitness-no-noun-inheritance")
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

