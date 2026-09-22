#!/usr/bin/env python3
"""Landmine UC1: verify_fast_blockers refuse missing interview-packet."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "interview-packet-missing"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("interview-packet" in b for b in blockers):
        print("ASSERT:FAIL expected UC1 interview-packet blocker")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS verify blocks missing interview-packet (UC1)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
