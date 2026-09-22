#!/usr/bin/env python3
"""X1–X3: NLC-0024-04..06 must stay named expansion/partial — no fake MET."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules" / "nlc-0024.json"
PARKED = {
    "NLC-0024-04": ("expansion",),
    "NLC-0024-05": ("expansion",),
    "NLC-0024-06": ("expansion", "partial"),
}


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not RULES.is_file():
        print("VIOLATION missing rules/nlc-0024.json")
        print("RESULT:NOT_MET")
        return 1
    data = json.loads(RULES.read_text(encoding="utf-8"))
    by_id = {r.get("id"): r for r in data.get("rules", []) if isinstance(r, dict)}
    for rid, prefixes in PARKED.items():
        row = by_id.get(rid)
        if not row:
            violations.append(f"missing {rid}")
            continue
        gate = str(row.get("gate") or "")
        if not any(gate.startswith(p) for p in prefixes):
            violations.append(f"{rid} gate must start with {prefixes}, got {gate!r}")
    schema = ROOT / "docs" / "nlc" / "emit-manifest.schema.json"
    if not schema.is_file():
        violations.append("missing docs/nlc/emit-manifest.schema.json")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
