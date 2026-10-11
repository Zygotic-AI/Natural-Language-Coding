"""ADR 0051 / SG2: gate-set bytes must match integrity/gate-change-receipts.json."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from nouns.gate_set.gate_set import iter_gate_set_relative_paths

RECEIPTS_REL = "integrity/gate-change-receipts.json"


def content_hash(body: bytes) -> str:
    """SHA-256 hex digest of file contents."""
    return hashlib.sha256(body).hexdigest()


def load_registry(root: Path) -> tuple[dict[str, Any] | None, list[str]]:
    """Load gate-change receipt registry; return (payload, errors)."""
    path = root / RECEIPTS_REL
    if not path.is_file():
        return None, ["missing gate-change receipts registry"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, ["invalid gate-change receipts JSON"]
    if not isinstance(payload, dict):
        return None, ["gate-change receipts root must be object"]
    receipts = payload.get("receipts")
    if not isinstance(receipts, dict):
        return None, ["gate-change receipts.receipts must be object"]
    return payload, []


def receipt_row(receipts: dict[str, Any], rel_path: str) -> dict[str, Any] | None:
    """Return receipt object for rel_path when present."""
    row = receipts.get(rel_path)
    return row if isinstance(row, dict) else None


def path_receipt_holds(root: Path, receipts: dict[str, Any], rel_path: str) -> bool:
    """True when on-disk bytes match recorded content_sha256 for rel_path."""
    row = receipt_row(receipts, rel_path)
    if row is None:
        return False
    recorded = row.get("content_sha256")
    if not isinstance(recorded, str) or not recorded:
        return False
    file_path = root / rel_path
    if not file_path.is_file():
        return False
    return content_hash(file_path.read_bytes()) == recorded


def gate_change_errors(root: Path, *, paths: list[str] | None = None) -> list[str]:
    """List violations for gate-set receipt confirmation (completion only)."""
    payload, load_errors = load_registry(root)
    if payload is None:
        return load_errors
    receipts_raw = payload.get("receipts")
    receipts = receipts_raw if isinstance(receipts_raw, dict) else {}
    check_paths = paths if paths is not None else iter_gate_set_relative_paths(root)
    errors: list[str] = []
    for rel in check_paths:
        if rel not in receipts:
            errors.append(f"{rel}: missing gate-change receipt")
            continue
        if not path_receipt_holds(root, receipts, rel):
            errors.append(f"{rel}: gate-change receipt does not match current hash")
    return errors


def main() -> int:
    """Exit 0 MET when every gate-set member matches the ratified registry."""
    root = Path(__file__).resolve().parents[3]
    errors = gate_change_errors(root)
    if errors:
        for item in errors[:25]:
            print(f"VIOLATION {item}")
        if len(errors) > 25:
            print(f"VIOLATION ... and {len(errors) - 25} more")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
