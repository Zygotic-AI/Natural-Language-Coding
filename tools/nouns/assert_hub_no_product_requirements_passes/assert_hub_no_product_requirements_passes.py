"""Landmine ADR 0016: hub must MET fitness-hub-no-product-requirements."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "fitness-hub-no-product-requirements.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-hub-no-product-requirements should MET")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS hub no product requirements MET (ADR 0016)")
    return 0


