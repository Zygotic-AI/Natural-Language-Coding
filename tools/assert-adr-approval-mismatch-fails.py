#!/usr/bin/env python3
"""Landmine: editing an approved ADR invalidates that record's receipt."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.adr_approval import active_numbers, receipt_holds


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    payload = json.loads((root / "integrity" / "adr-approval-receipts.json").read_text(encoding="utf-8"))
    receipts = payload["receipts"]
    numbers = active_numbers((root / "adrs" / "ACTIVE.md").read_text(encoding="utf-8"))
    wanted = sys.argv[1:]
    targets = wanted or numbers
    for number in targets:
        matches = list((root / "adrs").glob(f"{number}-*.md"))
        if len(matches) != 1:
            print(f"ASSERT:FAIL {number} file")
            return 1
        mutated = matches[0].read_bytes() + b"\nviolated\n"
        if receipt_holds(receipts, number, mutated):
            print(f"ASSERT:FAIL {number} edit still approved")
            return 1
    print(f"ASSERT:PASS approval invalidated for {len(targets)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
