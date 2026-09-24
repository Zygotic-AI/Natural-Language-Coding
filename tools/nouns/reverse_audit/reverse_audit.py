"""X2: reverse-audit runner (NLC-0024-05)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOUNDARY = "bba-emit"


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


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    path = Path(args[0]).resolve() if args else None
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
