"""Active ADR ratification is the owner's OpenPGP sidecar or batch (C6).

Hash-only `integrity/adr-approval-receipts.json` is retired. Presence of that
file is NOT_MET. This module does not load or honor receipt rows.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import re
import sys
from pathlib import Path

RETIRED_RECEIPTS_REL = "integrity/adr-approval-receipts.json"
_ROW = re.compile(r"^\|\s*(\d{4})\s*\|")


def content_hash(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def active_numbers(active_text: str) -> list[str]:
    numbers: list[str] = []
    for line in active_text.splitlines():
        match = _ROW.match(line.strip())
        if match:
            numbers.append(match.group(1))
    return numbers


def approval_errors(root: Path) -> list[str]:
    """Refuse the retired receipts file. Ratification is C6 sidecar/batch only."""
    if (root / RETIRED_RECEIPTS_REL).is_file():
        return [
            f"{RETIRED_RECEIPTS_REL} is retired; ratification is C6 sidecar/batch only"
        ]
    return []


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = approval_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
