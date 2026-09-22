#!/usr/bin/env python3
"""Landmine ADR 0023: hub repo must MET rule-coverage --check."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "nlc_rule_coverage.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(ROOT), "--check"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL hub rule-coverage --check should MET")
        print(proc.stdout)
        print(proc.stderr)
        return 1
    print("ASSERT:PASS hub rule-coverage MET --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
