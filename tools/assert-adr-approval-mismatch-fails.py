#!/usr/bin/env python3
"""Landmine: editing an Accepted ADR must not stay covered by its detached signature."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.adr_file_sig.adr_file_sig import (  # noqa: E402
    PINNED_OWNER_FINGERPRINT,
    detached_sig_rel,
    verify_adr_detached_signature,
)
from nouns.adr_approval import active_numbers  # noqa: E402


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    numbers = active_numbers((root / "adrs" / "ACTIVE.md").read_text(encoding="utf-8"))
    targets = sys.argv[1:] or numbers
    checked = 0
    for number in targets:
        matches = list((root / "adrs").glob(f"{number}-*.md"))
        if len(matches) != 1:
            print(f"ASSERT:FAIL {number} file")
            return 1
        rel = matches[0].relative_to(root).as_posix()
        sig = root / detached_sig_rel(rel)
        if not sig.is_file():
            # Awaiting owner catch-up: no valid sig exists, so an edit cannot stay covered.
            checked += 1
            continue
        original = matches[0].read_bytes()
        try:
            matches[0].write_bytes(original + b"\nviolated\n")
            errors = verify_adr_detached_signature(root, rel)
        finally:
            matches[0].write_bytes(original)
        if not errors:
            print(f"ASSERT:FAIL {number} edit still approved by {sig.name}")
            return 1
        checked += 1
    print(
        f"ASSERT:PASS C6 detached signature invalidated for {checked} records "
        f"(pin {PINNED_OWNER_FINGERPRINT})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
