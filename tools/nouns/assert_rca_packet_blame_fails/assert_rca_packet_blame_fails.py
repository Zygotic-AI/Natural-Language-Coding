"""Landmine ADR 0025: validator refuses agent-blame RCA packets."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BAD = ROOT / "examples" / "rca-packet-blame-agent" / "rca-packet.json"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate-rca-packet.py"), str(BAD)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL validate-rca-packet should refuse blame-agent specimen")
        return 1
    print("ASSERT:PASS validate-rca-packet refuses agent-blame RCA")
    return 0


