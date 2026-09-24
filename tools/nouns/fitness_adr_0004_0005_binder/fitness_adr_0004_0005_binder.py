#!/usr/bin/env python3
"""ADR 0004/0005: produce package validation + quality fixtures + landmines."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]

LANDMINES = (
    "assert-quality-metric-passes.py",
    "assert-produce-handoff-refused.py",
    "assert-produce-role-separation-refused.py",
    "assert-verify-deep-produce-refused.py",
    "assert-verify-deep-role-separation-refused.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = read_tool("tools/ci_fitness.py")
    for name in LANDMINES:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
    if "fitness-produce-ssot-binder" not in ci:
        violations.append("ci_fitness must run fitness-produce-ssot-binder")
    if not (ROOT / "tools/nlc_produce_package.py").is_file():
        violations.append("missing nlc_produce_package.py")
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

