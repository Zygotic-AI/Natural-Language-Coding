"""FINDINGS, DESCRIBE, and the hub record must match the release-prep script."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.release_prep_surfaces.release_prep_surfaces import match_errors  # noqa: E402


def main() -> int:
    _ = sys.argv[1:]
    errors = match_errors(ROOT)
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
