#!/usr/bin/env python3
"""Landmine ADR 0051: gate-set byte change without matching receipt must NOT_MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.gate_change_receipt.gate_change_receipt import (
    content_hash,
    load_registry,
    path_receipt_holds,
)
from nouns.gate_set.gate_set import iter_gate_set_relative_paths


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    payload, errors = load_registry(root)
    if payload is None or errors:
        print(f"ASSERT:FAIL registry unavailable: {errors}")
        return 1
    receipts_raw = payload.get("receipts")
    receipts = receipts_raw if isinstance(receipts_raw, dict) else {}
    paths = iter_gate_set_relative_paths(root)
    if not paths:
        print("ASSERT:FAIL empty gate set")
        return 1
    sample = paths[0]
    file_path = root / sample
    if not file_path.is_file():
        print(f"ASSERT:FAIL missing sample {sample}")
        return 1
    mutated = file_path.read_bytes() + b"\n# gate-change known-bad\n"
    if path_receipt_holds(root, receipts, sample):
        if content_hash(mutated) == receipts[sample].get("content_sha256"):
            print("ASSERT:FAIL mutation did not change hash")
            return 1
        print(f"ASSERT:PASS gate-change receipt rejects mutated bytes for {sample}")
        return 0
    print(f"ASSERT:FAIL baseline receipt already mismatched for {sample}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
