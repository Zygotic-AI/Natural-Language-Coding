#!/usr/bin/env python3
"""Landmine: editing an Accepted ADR must not stay covered by a C6 batch hash."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.adr_approval import active_numbers, content_hash
from nouns.owner_sidecar.owner_sidecar import (
    committed_batch_approval_rels,
    verify_batch_approval,
)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    numbers = active_numbers((root / "adrs" / "ACTIVE.md").read_text(encoding="utf-8"))
    wanted = sys.argv[1:]
    targets = wanted or numbers
    batch_rels = committed_batch_approval_rels(root)
    checked = 0
    for number in targets:
        matches = list((root / "adrs").glob(f"{number}-*.md"))
        if len(matches) != 1:
            print(f"ASSERT:FAIL {number} file")
            return 1
        rel = matches[0].relative_to(root).as_posix()
        mutated = content_hash(matches[0].read_bytes() + b"\nviolated\n")
        for batch_rel in batch_rels:
            entries, _berr = verify_batch_approval(root, batch_rel)
            if entries.get(rel) == mutated:
                print(f"ASSERT:FAIL {number} edit still approved by {batch_rel}")
                return 1
        checked += 1
    print(f"ASSERT:PASS C6 batch hash invalidated for {checked} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
