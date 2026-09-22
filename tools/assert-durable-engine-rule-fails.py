#!/usr/bin/env python3
"""Landmine UC13: durable goal without engine.runtime rule."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "durable-engine-missing-rule"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("UC13" in b or "durable engine" in b.lower() for b in blockers):
        print("ASSERT:FAIL expected UC13 durable engine rule blocker")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS durable engine rule required (UC13)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
