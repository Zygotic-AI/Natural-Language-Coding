"""Landmine ADR 0050: stale committed hub-content-tree-hash must fail with Reproduce."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HASH_PATH = ROOT / "integrity" / "hub-content-tree-hash.txt"


def main() -> int:
    if not HASH_PATH.is_file():
        print("ASSERT:FAIL missing hub-content-tree-hash.txt")
        return 1
    original = HASH_PATH.read_text(encoding="utf-8")
    try:
        HASH_PATH.write_text("0" * 64 + "\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "nlc_gate.py"), "hub-content-tree-fresh", "--tree", "."],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
    finally:
        HASH_PATH.write_text(original, encoding="utf-8")
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL hub-content-tree-fresh must NOT_MET on stale committed hash")
        print(combined[-600:])
        return 1
    if "Reproduce:" not in combined:
        print("ASSERT:FAIL stale evidence failure must print Reproduce:")
        print(combined[-600:])
        return 1
    print("ASSERT:PASS stale committed evidence fails with Reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
