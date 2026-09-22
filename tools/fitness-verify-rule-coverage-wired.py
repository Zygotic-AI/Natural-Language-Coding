#!/usr/bin/env python3
"""ADR 0023: ./nlc verify fast path calls rule_coverage_blockers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPLIANCE = ROOT / "tools" / "nlc_compliance.py"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not COMPLIANCE.is_file():
        violations.append("missing nlc_compliance.py")
    else:
        text = COMPLIANCE.read_text(encoding="utf-8", errors="replace")
        if "def rule_coverage_blockers" not in text:
            violations.append("nlc_compliance must define rule_coverage_blockers")
        if "rule_coverage_blockers(root)" not in text:
            violations.append("verify_fast_blockers must call rule_coverage_blockers")
    ci = (ROOT / "tools" / "ci_fitness.py").read_text(encoding="utf-8", errors="replace")
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
