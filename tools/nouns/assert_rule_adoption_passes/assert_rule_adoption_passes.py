"""Landmine ADR 0012: rule-coverage-minimal adopted rules ADOPTION:MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RULES = ROOT / "examples" / "rule-coverage-minimal" / "rules" / "adopted.json"
TOOL = ROOT / "tools" / "check-rule-adoption.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(RULES)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 or "ADOPTION:MET" not in out:
        print("ASSERT:FAIL rule-coverage-minimal rules should ADOPTION:MET")
        print(out)
        return 1
    print("ASSERT:PASS rule-coverage-minimal ADOPTION:MET")
    return 0


