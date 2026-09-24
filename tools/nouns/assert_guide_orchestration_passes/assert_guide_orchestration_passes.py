"""Landmine ADR 0019: guided orchestration fitness MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "fitness-guide-orchestration.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-guide-orchestration should MET")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS guide orchestration MET (ADR 0019)")
    return 0


