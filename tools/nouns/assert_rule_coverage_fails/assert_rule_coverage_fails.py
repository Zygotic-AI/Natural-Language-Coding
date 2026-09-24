"""Landmine: adopted rules without markers fail --check."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "rule-coverage-missing"
TOOL = ROOT / "tools" / "nlc_rule_coverage.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE), "--check", "--adr", "0023"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL rule-coverage-missing should NOT_MET --check")
        return 1
    print("ASSERT:PASS rule-coverage-missing fails --check without markers")
    return 0


