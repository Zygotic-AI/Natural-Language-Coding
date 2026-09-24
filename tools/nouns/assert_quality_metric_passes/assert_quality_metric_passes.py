"""Landmine ADR 0004/0005: quality-metric fixtures MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "fitness-quality-metric.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-quality-metric should MET")
        print(proc.stdout[-2000:])
        return 1
    print("ASSERT:PASS quality-metric fixtures MET (ADR 0004/0005)")
    return 0


