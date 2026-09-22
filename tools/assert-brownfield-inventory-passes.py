#!/usr/bin/env python3
"""Landmine UC15/0023: brownfield inventory runs and hints goal-scaffold."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "nlc-brownfield-inventory.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(ROOT / "examples" / "adopter-verify-fast-green")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    err = proc.stderr or ""
    if proc.returncode != 0:
        print("ASSERT:FAIL brownfield inventory exit non-zero")
        print(err)
        return 1
    if "goal-scaffold" not in err or "RULE-TRACE" not in err:
        print("ASSERT:FAIL brownfield stderr missing goal-scaffold / RULE-TRACE hint")
        print(err)
        return 1
    print("ASSERT:PASS brownfield inventory + ADR 0023 hints")
    return 0


if __name__ == "__main__":
    sys.exit(main())
