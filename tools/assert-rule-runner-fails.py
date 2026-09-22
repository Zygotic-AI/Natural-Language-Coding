#!/usr/bin/env python3
"""Landmine UC4: verify_fast refuses missing rule-ir.snapshot."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "rule-runner-missing-snapshot"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("rule runner" in b.lower() or "rule-ir" in b.lower() for b in blockers):
        print("ASSERT:FAIL expected UC4 rule-runner blocker")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS rule-runner snapshot required (UC4)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
