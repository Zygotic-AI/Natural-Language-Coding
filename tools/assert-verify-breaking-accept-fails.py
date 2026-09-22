#!/usr/bin/env python3
"""Landmine: breaking contract with ADR but no acceptance must fail verify (ADR 0006)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN = ROOT / "examples" / "verify-breaking-accept"


def main() -> int:
    nlc = ROOT / "tools" / "nlc.py"
    proc = subprocess.run(
        [sys.executable, str(nlc), "--project", str(SPECIMEN), "verify"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL verify should NOT_MET on verify-breaking-accept")
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "contract-break-accept" not in combined and "manager acceptance" not in combined.lower():
        print("ASSERT:FAIL verify should mention contract-break-accept / manager acceptance")
        print(combined[:900])
        return 1
    print("ASSERT:PASS verify refuses verify-breaking-accept without acceptance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
