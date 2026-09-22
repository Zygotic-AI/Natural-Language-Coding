#!/usr/bin/env python3
"""Landmine ADR 0017–0020: human-surface binder fitness MET."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "fitness-human-surface-binder.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ASSERT:FAIL fitness-human-surface-binder should MET")
        print(proc.stdout)
        return 1
    print("ASSERT:PASS human surface binders MET (ADR 0017–0020)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
