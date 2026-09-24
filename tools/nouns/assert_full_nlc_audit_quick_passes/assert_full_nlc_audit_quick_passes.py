"""Landmine: full-nlc-audit quick profile MET on hub main."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "full-nlc-audit.py"), "--check", "--profile", "quick"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 or "FULL_NLC_AUDIT:MET" not in out:
        print("ASSERT:FAIL full-nlc-audit --profile quick should MET")
        print(out[-2000:])
        return 1
    print("ASSERT:PASS full-nlc-audit quick MET")
    return 0


