#!/usr/bin/env python3
"""Landmine: v2 closure must not over-include root/doc paths (PM out-cases)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.gate_set.gate_set import is_gate_set_path  # noqa: E402

CASES = ROOT / "tools/fixtures/owner-ratification-gate-set/out-cases.json"


def main() -> int:
    if not CASES.is_file():
        print(f"ASSERT:FAIL missing {CASES.relative_to(ROOT)}")
        return 1
    out_cases = json.loads(CASES.read_text(encoding="utf-8")).get("out_cases") or []
    members = [rel for rel in out_cases if is_gate_set_path(ROOT, rel)]
    if members:
        print(f"ASSERT:FAIL over-included paths in gate set: {members}")
        return 1
    print("ASSERT:PASS excluded paths are not gate-set members")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
