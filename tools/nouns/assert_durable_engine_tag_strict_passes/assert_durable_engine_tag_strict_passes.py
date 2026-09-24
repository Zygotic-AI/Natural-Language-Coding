"""Landmine UC13 v2: matching engine.runtime.<name> tag passes strict gate."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "durable-engine-strict-ok"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_uc_blockers import engine_runtime_tag_strict_blockers

    blockers = engine_runtime_tag_strict_blockers(FIXTURE.resolve())
    if blockers:
        print("ASSERT:FAIL expected no engine.runtime strict blockers")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS engine.runtime strict tag match (UC13)")
    return 0
