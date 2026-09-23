#!/usr/bin/env python3
"""ADR 0029: ACTIVE tips must exist in INDEX; one tip per lineage; successor edges ok."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_adr_active import parse_active_rows, parse_index_rows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    _ = sys.argv[1:]
    index = parse_index_rows((ROOT / "adrs" / "INDEX.md").read_text(encoding="utf-8"))
    active_list = parse_active_rows((ROOT / "adrs" / "ACTIVE.md").read_text(encoding="utf-8"))
    violations: list[str] = []
    if not index:
        violations.append("INDEX has no parseable rows")
    if not active_list:
        violations.append("ACTIVE has no parseable rows")
    lineage_tips: dict[str, list[str]] = defaultdict(list)
    for row in active_list:
        adr = row["adr"]
        lineage = row["lineage"]
        if adr not in index:
            violations.append(f"ACTIVE {adr} missing from INDEX")
            continue
        ix = index[adr]
        if ix["status"] != "active":
            violations.append(f"ACTIVE {adr} INDEX status={ix['status']!r} (want active)")
        if ix["lineage"] != lineage:
            violations.append(f"ACTIVE {adr} lineage {lineage} != INDEX {ix['lineage']}")
        lineage_tips[lineage].append(adr)
    for lineage, tips in sorted(lineage_tips.items()):
        if len(tips) > 1:
            violations.append(f"lineage {lineage} has multiple ACTIVE tips: {tips}")
    for adr, ix in index.items():
        succ = ix["successor"]
        if succ and succ not in index and re.fullmatch(r"\d{4}", succ):
            violations.append(f"INDEX {adr} successor {succ} missing from INDEX")
        if ix["status"] == "superseded" and not succ:
            violations.append(f"INDEX {adr} superseded without successor")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print(f"RESULT:MET active={len(active_list)} index={len(index)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
