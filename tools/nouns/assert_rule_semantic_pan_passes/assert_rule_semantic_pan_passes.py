"""Landmine UC4 v2: semantic runner MET on compliant pan specimen."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "rule-semantic-pan-forbid-return-ok"


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
        print("ASSERT:FAIL semantic runner should MET on rule-semantic-pan-forbid-return-ok")
        return 1
    print("ASSERT:PASS semantic runner MET (UC4 v2)")
    return 0
