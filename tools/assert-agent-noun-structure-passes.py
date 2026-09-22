#!/usr/bin/env python3
"""Landmine ADR 0003: hub agent nouns MET fitness-agent-noun-structure."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "fitness-agent-noun-structure.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-agent-noun-structure should MET")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS agent noun structure MET (ADR 0003)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
