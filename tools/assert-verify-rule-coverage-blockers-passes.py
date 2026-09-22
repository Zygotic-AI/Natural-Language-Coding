#!/usr/bin/env python3
"""Landmine ADR 0023: rule-coverage-minimal has no rule_coverage verify blocker."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "rule-coverage-minimal"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import rule_coverage_blockers

    blockers = rule_coverage_blockers(FIXTURE.resolve())
    if blockers:
        print("ASSERT:FAIL rule-coverage-minimal should not rule_coverage-block verify")
        print(blockers)
        return 1
    print("ASSERT:PASS rule-coverage-minimal clear rule_coverage blocker")
    return 0


if __name__ == "__main__":
    sys.exit(main())
