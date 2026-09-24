"""Landmine ADR 0011: consumer-facing docs MET fitness-nlc-naming."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "fitness-nlc-naming.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-nlc-naming should MET on hub docs")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS fitness-nlc-naming MET (ADR 0011)")
    return 0


