#!/usr/bin/env python3
"""Fitness: X1 action-plan gate — ok specimen MET, bad specimen stays red."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "nlc-action-plan-gate.py"


def run(tree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(tree)],
        check=False, capture_output=True, text=True,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ok_code, ok_out = run(ROOT / "examples" / "action-plan-ok")
    if ok_code != 0 or "RESULT:MET" not in ok_out:
        violations.append("ok specimen did not MET")
    bad_code, bad_out = run(ROOT / "examples" / "action-plan-bad")
    if bad_code == 0 or "RESULT:NOT_MET" not in bad_out:
        violations.append("bad specimen did not stay red")
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
