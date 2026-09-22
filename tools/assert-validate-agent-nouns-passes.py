#!/usr/bin/env python3
"""Landmine: validate-agent-noun-packages MET on hub agents/."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "validate-agent-noun-packages.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL validate-agent-noun-packages should MET")
        print(proc.stdout)
        print(proc.stderr)
        return 1
    print("ASSERT:PASS validate-agent-noun-packages MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
