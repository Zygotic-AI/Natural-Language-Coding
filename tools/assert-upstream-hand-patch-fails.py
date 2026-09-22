#!/usr/bin/env python3
"""Landmine UC10: verify_deep refuses missing generate provenance."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "upstream-hand-patch-missing"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("UC10" in b or "provenance" in b.lower() for b in blockers):
        print("ASSERT:FAIL expected UC10 generate-provenance blocker")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS upstream hand-patch provenance required (UC10)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
