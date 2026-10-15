#!/usr/bin/env python3
"""Landmine ADR 0028: an atomic verb outside the baseline without an ADR fails."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.verb_set_lineage import extension_errors


def main() -> int:
    errors = extension_errors({"verbs": [{"name": "process", "adr": ""}]})
    if not errors:
        print("ASSERT:FAIL extension without an ADR must fail")
        return 1
    clean = extension_errors({"verbs": ["create", "read", "write", "update", "delete", "validate", "emit", "bind"]})
    if clean:
        print("ASSERT:FAIL baseline set must pass")
        return 1
    print("ASSERT:PASS verb-set extension without an ADR is refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
