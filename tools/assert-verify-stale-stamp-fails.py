#!/usr/bin/env python3
"""Landmine: product newer than before-generate stamp must fail verify."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN = ROOT / "examples" / "verify-stale-stamp"


def main() -> int:
    nlc = ROOT / "tools" / "nlc.py"
    proc = subprocess.run(
        [sys.executable, str(nlc), "--project", str(SPECIMEN), "verify"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL verify should NOT_MET with stale before-generate stamp")
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "before-generate" not in combined.lower() and "stamp" not in combined.lower():
        print("ASSERT:FAIL verify should mention stale stamp")
        print(combined[:800])
        return 1
    print("ASSERT:PASS verify refuses verify-stale-stamp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
