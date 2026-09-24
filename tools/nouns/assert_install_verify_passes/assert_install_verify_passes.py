"""Landmine ADR 0015: hub install hash manifest must MET on checkout."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "nlc-install-verify.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(ROOT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 or "INSTALL_VERIFY:MET" not in out:
        print("ASSERT:FAIL nlc-install-verify on hub checkout")
        print(out[-800:])
        return 1
    print("ASSERT:PASS install verify MET (ADR 0015)")
    return 0


