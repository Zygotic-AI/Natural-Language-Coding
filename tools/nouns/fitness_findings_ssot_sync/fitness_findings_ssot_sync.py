#!/usr/bin/env python3
"""Umbrella: FINDINGS vs tags + ADR-ENFORCEMENT table (F1 + F3)."""

from __future__ import annotations



import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "tools"


def run(name: str) -> int:
    proc = subprocess.run([sys.executable, str(TOOLS / name)], cwd=str(ROOT), check=False)
    return proc.returncode


def main() -> int:
    _ = sys.argv[1:]
    failed: list[str] = []
    for script in (
        "fitness-findings-shipped-tag-sync.py",
        "fitness-adr-enforcement-table-sync.py",
    ):
        if run(script) != 0:
            failed.append(script)
    if failed:
        print(f"VIOLATION failed: {', '.join(failed)}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

