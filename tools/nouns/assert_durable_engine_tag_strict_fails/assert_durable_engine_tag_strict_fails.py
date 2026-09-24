"""Landmine UC13 v2: bare engine.runtime tag fails when goal declares engine_runtime."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "durable-engine-vague-tag"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_uc_blockers import engine_runtime_tag_strict_blockers

    blockers = engine_runtime_tag_strict_blockers(FIXTURE.resolve())
    if not blockers or not any("engine.runtime strict" in b for b in blockers):
        print("ASSERT:FAIL expected UC13 engine.runtime strict blocker")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS engine.runtime strict rejects vague tag (UC13)")
    return 0
