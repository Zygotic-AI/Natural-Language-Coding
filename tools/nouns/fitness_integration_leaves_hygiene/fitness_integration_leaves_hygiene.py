#!/usr/bin/env python3
"""integration-leaves.json populated or explicit waive record (F4)."""

from __future__ import annotations



import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEAVES = ROOT / "integrity" / "integration-leaves.json"
WAIVE = ROOT / "integrity" / "integration-leaves-waive.json"


def main() -> int:
    _ = sys.argv[1:]
    if WAIVE.is_file():
        try:
            data = json.loads(WAIVE.read_text(encoding="utf-8"))
            if data.get("waived") and data.get("reason"):
                print("RESULT:MET")
                return 0
        except json.JSONDecodeError:
            print("VIOLATION integration-leaves-waive.json invalid JSON")
            print("RESULT:NOT_MET")
            return 1

    if not LEAVES.is_file():
        print("VIOLATION missing integration-leaves.json")
        print("RESULT:NOT_MET")
        return 1

    data = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = data.get("leaves") or []
    if leaves:
        print("RESULT:MET")
        return 0

    print("VIOLATION integration-leaves empty and no integration-leaves-waive.json")
    print("RESULT:NOT_MET")
    return 1


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

