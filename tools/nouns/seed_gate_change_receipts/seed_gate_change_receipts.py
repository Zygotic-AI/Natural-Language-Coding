"""Maintainer: write integrity/gate-change-receipts.json from current gate-set bytes."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import sys
from pathlib import Path

from nouns.gate_change_receipt.gate_change_receipt import content_hash
from nouns.gate_set.gate_set import iter_gate_set_relative_paths

RECEIPTS_REL = "integrity/gate-change-receipts.json"
BASELINE_NOTE = "baseline at ADR 0051 adoption, ratification pending"


def build_registry(root: Path) -> dict[str, object]:
    """Build full receipt map for the current gate-set member bytes."""
    receipts: dict[str, object] = {}
    for rel in iter_gate_set_relative_paths(root):
        file_path = root / rel
        if not file_path.is_file():
            continue
        receipts[rel] = {
            "content_sha256": content_hash(file_path.read_bytes()),
            "ratifier_role": "pending",
            "ratified_at": None,
            "note": BASELINE_NOTE,
        }
    return {
        "schema": 1,
        "baseline_note": BASELINE_NOTE,
        "receipts": receipts,
    }


def main() -> int:
    """Write gate-change receipt registry (maintainer path; not produce hand-edit)."""
    parser = argparse.ArgumentParser(description="Seed gate-change-receipts.json from tree")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    payload = build_registry(root)
    out_path = root / RECEIPTS_REL
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.dry_run:
        print(f"DRY_RUN would write {len(payload['receipts'])} receipts to {RECEIPTS_REL}")
        return 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"WROTE {RECEIPTS_REL} entries={len(payload['receipts'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
