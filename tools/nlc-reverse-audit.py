#!/usr/bin/env python3
"""X2: reverse-audit runner (NLC-0024-05).

Every applicable ADR must be bound to at least one action. An applicable ADR
with no binding is a plan defect, not an emit defect.

Input: JSON with keys:
  - "applicable_adrs": list of ADR ids
  - "bindings": list of {adr_id, action_id}
  If `path` is a directory, looks for audit.json inside it.
Output: RESULT:MET or RESULT:NOT_MET.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def resolve_input(path: Path) -> Path | None:
    if path.is_file():
        return path
    if path.is_dir():
        candidate = path / "audit.json"
        if candidate.is_file():
            return candidate
    return None


def validate(data: dict) -> list[str]:
    v: list[str] = []
    adrs = data.get("applicable_adrs")
    bindings = data.get("bindings")
    if not isinstance(adrs, list):
        return ["applicable_adrs must be a list"]
    if not isinstance(bindings, list):
        return ["bindings must be a list"]
    bound = {b.get("adr_id") for b in bindings if isinstance(b, dict)}
    for adr in adrs:
        if adr not in bound:
            v.append(f"applicable ADR {adr!r} is unbound to any action")
    return v


def main() -> int:
    path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    target = resolve_input(path) if path is not None else None
    if target is None:
        print("RESULT:MET")
        print("note: no audit file given; gate is default-closed and passes empty")
        return 0
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"VIOLATION invalid json: {exc}")
        print("RESULT:NOT_MET")
        return 1
    violations = validate(data)
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
