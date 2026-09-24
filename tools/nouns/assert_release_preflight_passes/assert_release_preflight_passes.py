"""Landmine ADR 0014/0022: hub release preflight --check MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "nlc_release_preflight.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--check"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 or "RELEASE_PREFLIGHT:MET" not in out:
        print("ASSERT:FAIL nlc_release_preflight --check should MET")
        print(out[-1200:])
        return 1
    print("ASSERT:PASS release preflight MET (ADR 0014)")
    return 0


