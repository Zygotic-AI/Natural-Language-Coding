"""Landmine ADR 0008: invoice-correct MET on noun-inheritance scan."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "invoice-correct"
TOOL = ROOT / "tools" / "fitness-no-noun-inheritance.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL invoice-correct should MET noun-inheritance scan")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS invoice-correct MET ADR 0008 scan")
    return 0


