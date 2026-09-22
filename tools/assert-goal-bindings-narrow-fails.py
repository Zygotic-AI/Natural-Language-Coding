#!/usr/bin/env python3
"""Landmine UC9: multi-goal repos require goal-bindings.json."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "goal-bindings-narrow-missing"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("goal-bindings" in b for b in blockers):
        print("ASSERT:FAIL expected UC9 goal-bindings blocker")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS goal-bindings required for multi-goal (UC9)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
