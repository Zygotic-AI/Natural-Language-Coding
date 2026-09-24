"""Landmine UC20: reference TypeScript call-tree pack inventory MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "call-tree-pack-reference"


def main() -> int:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc_call_tree.py"),
            "--check",
            "--root",
            str(FIXTURE),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 or "CALL_TREE:MET" not in out:
        print(out)
        print("ASSERT:FAIL call-tree reference pack should MET")
        return 1
    print("ASSERT:PASS call-tree pack reference (UC20)")
    return 0


