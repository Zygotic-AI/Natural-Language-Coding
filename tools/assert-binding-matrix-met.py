#!/usr/bin/env python3
"""Landmine ADR 0001 / R28: binding matrix audits must MET on hub."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "tools" / "audit-binding-matrix.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(AUDIT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        print("ASSERT:FAIL audit-binding-matrix exit non-zero")
        print(out[-1200:])
        return 1
    if "A-BINDING-UNBOUND:MET" not in out:
        print("ASSERT:FAIL missing A-BINDING-UNBOUND:MET")
        return 1
    if "RESULT:MET" not in out:
        print("ASSERT:FAIL missing RESULT:MET")
        return 1
    print("ASSERT:PASS binding matrix MET (ADR 0001)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
