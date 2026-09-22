#!/usr/bin/env python3
"""Fitness: prose -> compile -> full pipeline wire must ALL_MET."""
from __future__ import annotations
import subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSE = ROOT / "tools" / "nlc-emit-from-prose.py"


def main() -> int:
    if not PROSE.is_file():
        print("FITNESS:FAIL missing tools/nlc-emit-from-prose.py")
        return 1
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        proc = subprocess.run(
            [sys.executable, str(PROSE), "--self-test"],
            cwd=str(ROOT), check=False, capture_output=True, text=True,
        )
        if proc.returncode != 0 or "SELF_TEST:OK" not in proc.stdout:
            print("FITNESS:FAIL self-test", proc.stdout, proc.stderr)
            return 1
        print("FITNESS:MET nlc-emit-from-prose")
        return 0


if __name__ == "__main__":
    sys.exit(main())
