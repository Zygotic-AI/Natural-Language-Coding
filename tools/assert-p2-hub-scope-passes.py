#!/usr/bin/env python3
"""Landmine ADR 0002: P2 hub scope fitness MET."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "fitness-p2-hub-scope.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-p2-hub-scope should MET")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS P2 hub scope MET (ADR 0002)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
