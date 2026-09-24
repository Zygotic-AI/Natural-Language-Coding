"""Landmine: synthetic TODO/product SSOT mismatch must be detected."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import copy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "tools" / "fitness-todo-use-cases-ssot-matrix.py"


def main() -> int:
    proc = subprocess.run([sys.executable, str(MATRIX)], cwd=str(ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stdout or proc.stderr)
        print("ASSERT:FAIL matrix should MET")
        return 1

    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_todo_ssot import SECTION_START, check_todo_vs_status, load_status

    status = load_status()
    bad = copy.deepcopy(status)
    bad["ucs"]["UC1"]["product"] = "open"
    todo = f"{SECTION_START}\n- ✔ **UC1 (product)** — fake @done(26-09-21 10:00)\n"
    if not check_todo_vs_status(todo, bad):
        print("ASSERT:FAIL should detect UC1 product @done with product=open")
        return 1
    print("ASSERT:PASS todo-use-cases-ssot negative detection")
    return 0


