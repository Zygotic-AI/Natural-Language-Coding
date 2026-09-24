"""Landmine ADR 0017: dashboard fitness MET on hub."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "fitness-dashboard-interview-sync.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-dashboard-interview-sync should MET")
        print(proc.stdout)
        print(proc.stderr)
        return 1
    print("ASSERT:PASS dashboard interview sync MET")
    return 0


