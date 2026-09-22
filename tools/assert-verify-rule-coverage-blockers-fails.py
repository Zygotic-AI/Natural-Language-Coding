#!/usr/bin/env python3
"""Landmine ADR 0023: verify_fast includes rule-coverage blocker on missing markers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "rule-coverage-missing"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import rule_coverage_blockers

    blockers = rule_coverage_blockers(FIXTURE.resolve())
    if not blockers:
        print("ASSERT:FAIL rule-coverage-missing should block verify (rule_coverage)")
        return 1
    joined = " ".join(blockers).casefold()
    if "missing nlc:rule" not in joined and "missing marker" not in joined:
        print(f"ASSERT:FAIL unexpected blockers: {blockers}")
        return 1
    print("ASSERT:PASS verify rule_coverage blocker on missing markers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
