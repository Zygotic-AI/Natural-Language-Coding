#!/usr/bin/env python3
"""Landmine ADR 0018: ./nlc human gaps are interview-shaped, not NOT_MET-first."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NLC = ROOT / "nlc"


def main() -> int:
    if not NLC.is_file():
        print("ASSERT:FAIL missing ./nlc launcher")
        return 1
    proc = subprocess.run(
        [str(NLC), "new"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    stderr = proc.stderr or ""
    lines = [ln.strip() for ln in stderr.splitlines() if ln.strip()]
    if not lines:
        print("ASSERT:FAIL expected interview stderr from ./nlc new")
        return 1
    first = lines[0]
    if re_not_met_head(first):
        print(f"ASSERT:FAIL first stderr line must not be a gate token: {first}")
        return 1
    if "What's wrong:" not in stderr and "?" not in stderr:
        print("ASSERT:FAIL expected gap list or ask question in stderr")
        print(stderr)
        return 1
    if proc.returncode == 0:
        print("ASSERT:FAIL ./nlc new without folder should exit non-zero")
        return 1
    print("ASSERT:PASS ./nlc new emits ADR 0018 interview gap")
    return 0


def re_not_met_head(line: str) -> bool:
    return ":NOT_MET" in line and line.split(":", 1)[0].isupper()


if __name__ == "__main__":
    sys.exit(main())
