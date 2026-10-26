#!/usr/bin/env python3
"""Content-only change plus hash sync must not trip the gate-set signature check.

PR #30 option A: integrity/hub-content-tree-hash.txt is a freshness stamp, not a
signed gate-set member. A non-member edit that rewrites that stamp must leave
manifest bytes unchanged so the existing owner sidecar still applies.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.gate_set.gate_set import CONTENT_TREE_HASH_REL, derive_gate_set_paths  # noqa: E402
from nouns.gate_set_manifest.gate_set_manifest import (  # noqa: E402
    MANIFEST_REL,
    _manifest_path_set,
    gate_set_manifest_errors,
    manifest_bytes,
)

CONTENT_ONLY_REL = "LICENSE"


def _fail_closed(value: object, *, label: str) -> bool:
    """True only for a known non-empty success. Missing, empty, or unknown is false."""
    if value is None:
        print(f"ASSERT:FAIL {label}: missing tool or None result counts as false")
        return False
    if value == "" or value == [] or value == ():
        print(f"ASSERT:FAIL {label}: empty result counts as false")
        return False
    if value is False:
        print(f"ASSERT:FAIL {label}: unknown/false result counts as false")
        return False
    return True


def main() -> int:
    try:
        derived = derive_gate_set_paths(ROOT)
    except Exception as exc:  # missing tool / import failure is fail-closed
        print(f"ASSERT:FAIL derive_gate_set_paths missing or failed: {exc}")
        return 1
    if not _fail_closed(derived, label="derive_gate_set_paths"):
        return 1
    if CONTENT_TREE_HASH_REL in derived:
        print(f"ASSERT:FAIL {CONTENT_TREE_HASH_REL} is still a derived gate-set member")
        return 1
    if CONTENT_ONLY_REL in derived:
        print(f"ASSERT:FAIL content-only specimen {CONTENT_ONLY_REL} is a gate-set member")
        return 1

    manifest_path = ROOT / MANIFEST_REL
    hash_path = ROOT / CONTENT_TREE_HASH_REL
    content_path = ROOT / CONTENT_ONLY_REL
    if not manifest_path.is_file() or not hash_path.is_file() or not content_path.is_file():
        print("ASSERT:FAIL missing manifest, hash stamp, or content-only specimen")
        return 1

    on_disk_paths = _manifest_path_set(manifest_path.read_bytes())
    if not _fail_closed(sorted(on_disk_paths), label="manifest path column"):
        return 1
    if CONTENT_TREE_HASH_REL in on_disk_paths:
        print(f"ASSERT:FAIL {CONTENT_TREE_HASH_REL} is still in the manifest path column")
        return 1

    content_override = content_path.read_bytes() + b"\n# content-only change\n"
    hash_override = b"0" * 64 + b"\n"
    overrides = {CONTENT_ONLY_REL: content_override, CONTENT_TREE_HASH_REL: hash_override}

    try:
        baseline = manifest_bytes(ROOT)
        after = manifest_bytes(ROOT, overrides=overrides)
    except Exception as exc:
        print(f"ASSERT:FAIL manifest_bytes missing or failed: {exc}")
        return 1
    if not _fail_closed(baseline, label="manifest_bytes baseline"):
        return 1
    if baseline != after:
        print("ASSERT:FAIL content-only plus hash sync changed gate-set manifest bytes")
        return 1

    try:
        errors = gate_set_manifest_errors(ROOT, overrides=overrides)
    except Exception as exc:
        print(f"ASSERT:FAIL gate_set_manifest_errors missing or failed: {exc}")
        return 1
    if errors is None:
        print("ASSERT:FAIL gate_set_manifest_errors: missing tool or None result counts as false")
        return 1
    membership = [
        item
        for item in errors
        if "bytes do not match" in item
        or "derived gate-set" in item
        or "extra path" in item
    ]
    if membership:
        print(f"ASSERT:FAIL content-only plus hash sync tripped membership/bytes: {membership!r}")
        return 1
    print(
        "ASSERT:PASS content-only change plus hash sync leaves manifest bytes "
        "and membership unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
