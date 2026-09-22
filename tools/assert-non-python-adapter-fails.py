#!/usr/bin/env python3
"""Landmine UC16: non-Python source without language-adapters.json."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "non-python-without-adapter"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("UC16" in b for b in blockers):
        print("ASSERT:FAIL expected UC16 non-Python adapter blocker")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS non-Python requires adapter (UC16)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
