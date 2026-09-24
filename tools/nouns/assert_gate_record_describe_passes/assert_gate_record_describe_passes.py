"""Landmine ADR 0010: gate-record --describe prints binder doc."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "nlc_gate_record.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--describe"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 or "nlc_gate_record.py" not in out:
        print("ASSERT:FAIL gate-record --describe should print binder")
        print(out[-800:])
        return 1
    print("ASSERT:PASS gate-record --describe (ADR 0010)")
    return 0


