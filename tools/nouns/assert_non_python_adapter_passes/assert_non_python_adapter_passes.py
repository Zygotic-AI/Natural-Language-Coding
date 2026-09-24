"""Landmine UC16: approved non-Python adapter clears UC16 blocker."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "non-python-with-adapter"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    uc16 = [b for b in blockers if "UC16" in b]
    if uc16:
        print("ASSERT:FAIL expected no UC16 blocker on non-python-with-adapter")
        for b in uc16:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS non-Python adapter approved (UC16 reference)")
    return 0


