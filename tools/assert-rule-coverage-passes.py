#!/usr/bin/env python3
"""Landmine: rule-coverage-minimal must MET --check."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "rule-coverage-minimal"
TOOL = ROOT / "tools" / "nlc_rule_coverage.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE), "--check", "--adr", "0023"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL rule-coverage-minimal should MET --check")
        print(proc.stdout)
        print(proc.stderr)
        return 1
    print("ASSERT:PASS rule-coverage-minimal MET --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
