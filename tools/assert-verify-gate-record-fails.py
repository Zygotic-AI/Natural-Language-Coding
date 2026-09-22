#!/usr/bin/env python3
"""Landmine: app tree with goals/implementation.py must fail verify without gate records."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN = ROOT / "examples" / "goal-untested"


def main() -> int:
    nlc = ROOT / "tools" / "nlc.py"
    proc = subprocess.run(
        [sys.executable, str(nlc), "--project", str(SPECIMEN), "verify"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL verify should NOT_MET without gate records on goal-untested")
        return 1
    print("ASSERT:PASS verify refuses goal-untested without gate records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
