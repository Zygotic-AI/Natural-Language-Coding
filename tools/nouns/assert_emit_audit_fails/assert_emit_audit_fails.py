"""Landmine: specimen missing audit.status must be NOT_MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = ROOT / "examples" / "emit-manifest-missing-audit"
TOOL = ROOT / "tools" / "nlc_emit_audit.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(SPEC)],
        check=False,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 and "RESULT:NOT_MET" in out:
        print("ASSERT:PASS")
        return 0
    print("ASSERT:FAIL expected NOT_MET on missing-audit specimen")
    print(out)
    return 1


