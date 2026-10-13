"""Completion confirmation that active ADR bytes still match the hash registry.

This is not ratification. Ratification is only the owner's OpenPGP sidecar
(ADR 0052). `integrity/adr-approval-receipts.json` records that a hash update
completed; it does not authorize Accepted status.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import re
import sys
from pathlib import Path

RECEIPTS_REL = "integrity/adr-approval-receipts.json"
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


def receipt_holds(receipts: dict[str, object], number: str, body: bytes) -> bool:
    row = receipts.get(number)
    if not isinstance(row, dict):
        return False
    recorded = row.get("content_sha256")
    return isinstance(recorded, str) and recorded == content_hash(body)


def approval_errors(root: Path) -> list[str]:
    receipts_path = root / RECEIPTS_REL
    if not receipts_path.is_file():
        return ["missing approval receipts"]
    payload = json.loads(receipts_path.read_text(encoding="utf-8"))
    receipts = payload.get("receipts") if isinstance(payload, dict) else None
    if not isinstance(receipts, dict):
        return ["approval receipts must be an object"]
    numbers = active_numbers((root / "adrs" / "ACTIVE.md").read_text(encoding="utf-8"))
    errors: list[str] = []
    for number in numbers:
        matches = sorted((root / "adrs").glob(f"{number}-*.md"))
        if len(matches) != 1:
            errors.append(f"{number}: expected one ADR file")
            continue
        if not receipt_holds(receipts, number, matches[0].read_bytes()):
            errors.append(f"{number}: approval receipt does not match the current hash")
    return errors


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
