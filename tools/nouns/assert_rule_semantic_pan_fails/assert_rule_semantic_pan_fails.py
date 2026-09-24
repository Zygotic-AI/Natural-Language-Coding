"""Landmine UC4 v2: semantic runner NOT_MET when pan field is returned."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "rule-semantic-pan-forbid-return"


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
    if proc.returncode == 0:
        print(out)
        print("ASSERT:FAIL semantic runner should NOT_MET on pan return violation")
        return 1
    if "semantic rule runner" not in out and "RULE_RUNNER:NOT_MET" not in out:
        print(out)
        print("ASSERT:FAIL expected semantic UC4 failure")
        return 1
    print("ASSERT:PASS semantic runner refuses pan return (UC4 v2)")
    return 0
