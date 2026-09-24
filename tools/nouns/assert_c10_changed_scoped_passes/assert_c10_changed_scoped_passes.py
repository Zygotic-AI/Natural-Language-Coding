"""Landmine ADR 0006: diff-scoped C10 MET when break is outside CHANGED."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "c10-changed-out-of-scope"
TOOL = ROOT / "tools" / "fitness-c10-changed.py"
TREE = ROOT / "tools" / "fitness-c10.py"


def main() -> int:
    scoped = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if scoped.returncode != 0:
        print("ASSERT:FAIL fitness-c10-changed should MET on c10-changed-out-of-scope")
        print(scoped.stdout)
        return 1
    tree = subprocess.run(
        [sys.executable, str(TREE), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if tree.returncode == 0:
        print("ASSERT:FAIL fitness-c10 tree-wide should NOT_MET (breaking goals/bad)")
        return 1
    print("ASSERT:PASS C10 diff-scoped vs tree-wide on c10-changed-out-of-scope")
    return 0


