#!/usr/bin/env python3
"""Landmine: v2 closure must not over-include root/doc paths (PM out-cases)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.gate_set.gate_set import is_gate_set_path  # noqa: E402

# PM closure v2 out-cases at 23a11c8 (closure.txt removed on branch).
OUT_CASES = (
    "LICENSE",
    "MANIFESTO.md",
    "HOLES.md",
)


def main() -> int:
    members = [rel for rel in OUT_CASES if is_gate_set_path(ROOT, rel)]
    if members:
        print(f"ASSERT:FAIL over-included paths in gate set: {members}")
        return 1
    print("ASSERT:PASS excluded paths are not gate-set members")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
