#!/usr/bin/env python3
"""Waived expansion keys must be empty in uc-product-status."""

from __future__ import annotations



import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WAIVES = ROOT / "integrity" / "product-expansion-waives.json"
STATUS = ROOT / "integrity" / "uc-product-status.json"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not WAIVES.is_file():
        violations.append("missing product-expansion-waives.json")
        return 1
    waives = json.loads(WAIVES.read_text(encoding="utf-8")).get("waives") or []
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    ucs = status.get("ucs") or {}
    for row in waives:
        key = row.get("key", "")
        if not key or "." not in key:
            violations.append(f"invalid waive key {key}")
            continue
        uc, exp_key = key.split(".", 1)
        block = ucs.get(uc) or {}
        if exp_key in (block.get("expansion_only") or []):
            violations.append(f"waived key still in expansion_only: {key}")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

