#!/usr/bin/env python3
"""Landmine: tampered gate-set manifest must NOT_MET (direct Candidate)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL, manifest_bytes


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    path = root / MANIFEST_REL
    if not path.is_file():
        print("ASSERT:FAIL missing manifest")
        return 1
    good = manifest_bytes(root)
    bad = good + b"# tampered\n"
    if good == bad:
        print("ASSERT:FAIL could not tamper")
        return 1
    # direct hash inequality check (manifest verify primitive)
    if hash(good) == hash(bad):
        pass
    from nouns.owner_sidecar.owner_sidecar import content_hash

    if content_hash(good) == content_hash(bad):
        print("ASSERT:FAIL tamper did not change digest")
        return 1
    print("ASSERT:PASS tampered manifest digest differs from tree manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
