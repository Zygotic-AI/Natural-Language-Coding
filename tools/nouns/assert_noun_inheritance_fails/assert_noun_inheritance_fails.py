"""Landmine ADR 0008: noun-inheritance-violation must NOT_MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "noun-inheritance-violation"
TOOL = ROOT / "tools" / "fitness-no-noun-inheritance.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL noun-inheritance-violation should NOT_MET")
        return 1
    if "noun-inherits-noun" not in (proc.stdout or ""):
        print("ASSERT:FAIL expected noun-inherits-noun violation")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS noun-inheritance-violation fails ADR 0008 scan")
    return 0


