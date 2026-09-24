"""invoice-correct is AI-green and must not RELEASE without Released-by."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TREE = ROOT / "examples" / "invoice-correct"
AUDIT = ROOT / "tools" / "release-audit.py"


def main() -> int:
    if not TREE.is_dir():
        print(f"ASSERT:FAIL missing {TREE}")
        return 1
    proc = subprocess.run(
        [sys.executable, str(AUDIT), str(TREE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    print(out.rstrip())
    if proc.returncode == 0:
        print("ASSERT:FAIL invoice-correct released without a human")
        return 1
    if "H-RELEASE" not in out or "RELEASE:NOT_MET" not in out:
        print("ASSERT:FAIL expected H-RELEASE and RELEASE:NOT_MET")
        return 1
    print("ASSERT:PASS release-audit still blocks unsigned invoice-correct")
    return 0


