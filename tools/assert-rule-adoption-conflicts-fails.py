#!/usr/bin/env python3
"""Landmine ADR 0012: rule-adoption-conflict specimen must ADOPTION:NOT_MET."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "rule-adoption-conflict" / "rules" / "adopted.json"
TOOL = ROOT / "tools" / "check-rule-adoption.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0 or "ADOPTION:NOT_MET" not in out:
        print("ASSERT:FAIL rule-adoption-conflict should ADOPTION:NOT_MET")
        print(out)
        return 1
    print("ASSERT:PASS rule-adoption-conflict fails adopt-time check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
