"""Landmine UC3/pack consume: bind_ready + requirements-sync-pending blocked."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "requirements-sync-pending"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("requirements-sync" in b or "UC3 requirements" in b for b in blockers):
        print("ASSERT:FAIL expected requirements-sync blocker")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS requirements-sync-pending vs bind_ready (UC3/pack)")
    return 0


