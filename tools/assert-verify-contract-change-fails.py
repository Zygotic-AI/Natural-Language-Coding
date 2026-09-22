#!/usr/bin/env python3
"""Landmine: product tree with bad impact list must fail verify (ADR 0006 / C21)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN = ROOT / "examples" / "verify-impact-c21"


def main() -> int:
    nlc = ROOT / "tools" / "nlc.py"
    proc = subprocess.run(
        [sys.executable, str(nlc), "--project", str(SPECIMEN), "verify"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL verify should NOT_MET on verify-impact-c21")
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "C21" not in combined and "missing-caller" not in combined.lower():
        print("ASSERT:FAIL verify should mention C21 / missing caller")
        print(combined[:900])
        return 1
    print("ASSERT:PASS verify refuses verify-impact-c21 (ADR 0006 C21)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
