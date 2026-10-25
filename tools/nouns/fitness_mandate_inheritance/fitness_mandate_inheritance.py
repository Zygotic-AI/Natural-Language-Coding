"""Produce-time refuse: touching a mandated path without moving its pins."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

from nouns.mandated_paths.mandated_paths import (
    pin_move_errors,
    snapshot_errors,
    unsigned_manifest_incomplete,
)

ROOT = Path(__file__).resolve().parents[3]


def _hub_repo(root: Path) -> bool:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from nlc_pipeline import is_hub_repo

    return is_hub_repo(root)


def main() -> int:
    args = sys.argv[1:]
    root = Path(args[0]).resolve() if args and not args[0].startswith("-") else ROOT
    if not _hub_repo(root):
        print("MANDATE_INHERITANCE:MET skip (hub-only gate, not hub tree)")
        return 0
    errors = snapshot_errors(root)
    errors.extend(pin_move_errors(root))
    incomplete = unsigned_manifest_incomplete(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("MANDATE_INHERITANCE:NOT_MET")
        return 1
    for item in incomplete:
        print(item)
    if incomplete:
        print("MANDATE_INHERITANCE:INCOMPLETE")
        return 0
    print("MANDATE_INHERITANCE:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
