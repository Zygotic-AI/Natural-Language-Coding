"""Landmine ADR 0006: diff-scoped C21 MET when missing caller is outside CHANGED."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "c21-changed-out-of-scope"
SCOPED = ROOT / "tools" / "fitness-c21-changed.py"
TREE = ROOT / "tools" / "fitness-c21.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(SCOPED), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-c21-changed should MET")
        print(proc.stdout)
        return 1
    tree = subprocess.run(
        [sys.executable, str(TREE), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if tree.returncode == 0:
        print("ASSERT:FAIL fitness-c21 tree-wide should NOT_MET (Order.ship)")
        return 1
    print("ASSERT:PASS C21 diff-scoped vs tree-wide on c21-changed-out-of-scope")
    return 0


