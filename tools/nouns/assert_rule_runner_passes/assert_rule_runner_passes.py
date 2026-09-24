"""Landmine UC4: rule-runner --check MET when snapshot present."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "adopter-verify-fast-green"


def main() -> int:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc_rule_runner.py"),
            "--check",
            "--root",
            str(FIXTURE),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 or "RULE_RUNNER:MET" not in out:
        print(out)
        print("ASSERT:FAIL rule-runner --check should MET on adopter-verify-fast-green")
        return 1
    print("ASSERT:PASS rule-runner snapshot check (UC4)")
    return 0


