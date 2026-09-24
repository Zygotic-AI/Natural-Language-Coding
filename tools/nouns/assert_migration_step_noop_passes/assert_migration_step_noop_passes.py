"""Landmine ADR 0014: noop migration step emits UPGRADE lines and completes."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_distribution import run_migration_step

    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            run_migration_step(ROOT, "0.1.0", "0.1.1")
    except SystemExit as exc:
        print(f"ASSERT:FAIL migration step exited {exc.code}")
        return 1
    out = buf.getvalue()
    if "UPGRADE:STEP" not in out or "kind=noop" not in out:
        print("ASSERT:FAIL missing UPGRADE:STEP noop log")
        print(out)
        return 1
    if "UPGRADE:STEP_COMPLETED" not in out:
        print("ASSERT:FAIL missing UPGRADE:STEP_COMPLETED")
        return 1
    print("ASSERT:PASS migration 0.1.0_to_0.1.1 noop step")
    return 0


