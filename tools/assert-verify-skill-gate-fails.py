#!/usr/bin/env python3
"""Landmine: gate-scoped SKILL.md must fail verify without gate-record (ADR 0010)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN = ROOT / "examples" / "verify-skill-ungated"


def main() -> int:
    nlc = ROOT / "tools" / "nlc.py"
    proc = subprocess.run(
        [sys.executable, str(nlc), "--project", str(SPECIMEN), "verify"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL verify should NOT_MET on verify-skill-ungated")
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "gate" not in combined.lower():
        print("ASSERT:FAIL verify should mention gate records")
        print(combined[:900])
        return 1
    print("ASSERT:PASS verify refuses verify-skill-ungated without gate record")
    return 0


if __name__ == "__main__":
    sys.exit(main())
