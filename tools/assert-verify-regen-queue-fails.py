#!/usr/bin/env python3
"""Landmine: open delta-regen queue must fail ./nlc verify (ADR 0006 loud prove)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN = ROOT / "examples" / "regen-queue-pending"


def main() -> int:
    nlc = ROOT / "tools" / "nlc.py"
    proc = subprocess.run(
        [sys.executable, str(nlc), "--project", str(SPECIMEN), "verify"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL verify should NOT_MET with pending delta-regen steps")
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "rebuild" not in combined.lower() and "queued" not in combined.lower():
        print("ASSERT:FAIL verify should mention queued rebuild(s)")
        return 1
    print("ASSERT:PASS verify refuses open delta-regen queue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
