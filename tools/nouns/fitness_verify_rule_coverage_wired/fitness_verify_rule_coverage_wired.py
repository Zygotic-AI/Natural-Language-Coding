#!/usr/bin/env python3
"""ADR 0023: ./nlc verify fast path calls rule_coverage_blockers."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]
COMPLIANCE = ROOT / "tools" / "nlc_compliance.py"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not COMPLIANCE.is_file():
        violations.append("missing nlc_compliance.py")
    else:
        text = read_tool("tools/nlc_compliance.py")
        if "def rule_coverage_blockers" not in text:
            violations.append("nlc_compliance must define rule_coverage_blockers")
        if "rule_coverage_blockers(root)" not in text:
            violations.append("verify_fast_blockers must call rule_coverage_blockers")
    ci = read_tool("tools/ci_fitness.py")
    for name in (
        "assert-verify-rule-coverage-blockers-fails",
        "assert-verify-rule-coverage-blockers-passes",
    ):
        if name not in ci:
            violations.append(f"ci_fitness must run {name}")
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

