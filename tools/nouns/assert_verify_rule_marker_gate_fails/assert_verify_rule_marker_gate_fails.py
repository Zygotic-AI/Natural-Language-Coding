"""Landmine: files with nlc:rule= markers must fail verify without gate records (ADR 0023)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPECIMEN = ROOT / "examples" / "rule-marker-domain"


def main() -> int:
    nlc = ROOT / "tools" / "nlc.py"
    proc = subprocess.run(
        [sys.executable, str(nlc), "--project", str(SPECIMEN), "verify"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print(
            "ASSERT:FAIL verify should NOT_MET without gate records on rule-marker-domain"
        )
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "gate" not in combined.lower():
        print("ASSERT:FAIL expected gate-record blocker in verify output")
        print(combined[:800])
        return 1
    print("ASSERT:PASS verify refuses rule-marker-domain without gate records")
    return 0


