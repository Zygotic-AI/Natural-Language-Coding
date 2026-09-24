#!/usr/bin/env python3
"""ADR 0006: contract-change fitness + landmines wired in CI."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]

SCRIPTS = (
    "fitness-c10-changed.py",
    "fitness-c21-changed.py",
    "nlc_contract_change.py",
    "nlc_contract_break_accept.py",
)

LANDMINES = (
    "assert-c10-changed-scoped-passes.py",
    "assert-c21-changed-scoped-passes.py",
    "assert-verify-contract-change-fails.py",
    "assert-verify-breaking-accept-fails.py",
    "assert-invoice-correct-contract-blockers-passes.py",
    "assert-contract-change-detects-c21-fails.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = read_tool("tools/ci_fitness.py")
    for name in SCRIPTS:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
    for name in LANDMINES:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
        elif "assert-c10-changed" in name and "assert-c10-changed" not in ci:
            violations.append("ci_fitness must run assert-c10-changed-scoped")
        elif "assert-c21-changed" in name and "assert-c21-changed" not in ci:
            violations.append("ci_fitness must run assert-c21-changed-scoped")
    change = read_tool("tools/nlc_contract_change.py")
    if "fitness-c10-changed" not in change:
        violations.append("nlc_contract_change must select fitness-c10-changed")
    if "fitness-c21-changed" not in change:
        violations.append("nlc_contract_change must select fitness-c21-changed")
    if "contract_change_applies" not in change:
        violations.append("nlc_contract_change must use contract_change_applies")
    ci = read_tool("tools/ci_fitness.py")
    if "fitness-specimen-contract-policy" not in ci:
        violations.append("ci_fitness must run fitness-specimen-contract-policy")
    if "fitness-verify-pipeline-wired" not in ci:
        violations.append("ci_fitness must run fitness-verify-pipeline-wired")
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

