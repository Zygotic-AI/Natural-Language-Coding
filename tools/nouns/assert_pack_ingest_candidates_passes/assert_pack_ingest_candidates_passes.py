"""Landmine: pack ingest candidates fixture validates."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "tools" / "fixtures" / "pack-ingest-candidates-valid.json"
TOOL = ROOT / "tools" / "validate-pack-ingest-candidates.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stdout or proc.stderr)
        print("ASSERT:FAIL pack ingest candidates validation")
        return 1
    print("ASSERT:PASS pack-ingest-candidates schema")
    return 0


