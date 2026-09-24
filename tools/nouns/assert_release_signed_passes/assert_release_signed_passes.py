"""A copy of invoice-correct with Released-by: a human must RELEASE:MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "examples" / "invoice-correct"
AUDIT = ROOT / "tools" / "release-audit.py"


def main() -> int:
    if not SRC.is_dir():
        print("ASSERT:FAIL missing invoice-correct")
        return 1
    tmp = Path(tempfile.mkdtemp(prefix="bbp-release-"))
    try:
        dest = tmp / "tree"
        shutil.copytree(SRC, dest)
        confirm = dest / "CONFIRM.md"
        confirm.write_text(confirm.read_text() + "\nReleased-by: Example Human\n")
        proc = subprocess.run(
            [sys.executable, str(AUDIT), str(dest)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        print(out.rstrip())
        if proc.returncode != 0 or "RELEASE:MET" not in out:
            print("ASSERT:FAIL expected RELEASE:MET after human Released-by")
            return 1
        print("ASSERT:PASS signed copy of invoice-correct releases")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


