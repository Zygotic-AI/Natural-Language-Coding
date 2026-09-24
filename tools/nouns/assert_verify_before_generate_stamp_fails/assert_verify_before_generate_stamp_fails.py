"""Landmine: product without before-generate stamp must fail verify (UC18 / ADR 0010)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPECIMEN = ROOT / "examples" / "verify-no-before-stamp"


def main() -> int:
    nlc = ROOT / "tools" / "nlc.py"
    proc = subprocess.run(
        [sys.executable, str(nlc), "--project", str(SPECIMEN), "verify"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL verify should NOT_MET without before-generate stamp")
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "before-generate" not in combined.lower():
        print("ASSERT:FAIL verify should mention before-generate stamp")
        print(combined[:800])
        return 1
    print("ASSERT:PASS verify refuses verify-no-before-stamp")
    return 0


