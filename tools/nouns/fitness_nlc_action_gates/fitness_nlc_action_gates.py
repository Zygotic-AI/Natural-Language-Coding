#!/usr/bin/env python3
"""Fitness: nlc-action-gates.py exists and refuses empty input (default-closed)."""

from __future__ import annotations



import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GATE = ROOT / "tools" / "nlc-action-gates.py"


def main() -> int:
    if not GATE.is_file():
        print("fitness-nlc-action-gates: MISSING tools/nlc-action-gates.py")
        return 1
    # empty list must fail (default-closed)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "empty.json"
        p.write_text("[]", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(GATE), str(p)],
            capture_output=True, text=True,
        )
    if proc.returncode == 0 or "RESULT:NOT_MET" not in (proc.stdout or ""):
        print("fitness-nlc-action-gates: empty list should fail, did not")
        print(proc.stdout)
        return 1
    print("fitness-nlc-action-gates: MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

