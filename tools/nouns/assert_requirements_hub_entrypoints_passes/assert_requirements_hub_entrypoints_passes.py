"""Landmine ADR 0013: hub nlc*.py CLIs call hub_tool()."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "fitness-requirements-hub-entrypoints.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-requirements-hub-entrypoints should MET")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS hub nlc CLI entrypoints call hub_tool")
    return 0


