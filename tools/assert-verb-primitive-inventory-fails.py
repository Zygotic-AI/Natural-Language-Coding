#!/usr/bin/env python3
"""Landmine ADR 0009: a verb that calls an undeclared primitive fails the inventory."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.call_tree import check_inventory


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        domain = root / "domain"
        domain.mkdir()
        (domain / "pay.py").write_text("def pay():\n    write()\n", encoding="utf-8")
        listed = root / ".nlc"
        listed.mkdir()
        (listed / "verb-primitives.json").write_text(
            '{"schema": 1, "verbs": {}}\n',
            encoding="utf-8",
        )
        errors = check_inventory(root)
    if not errors:
        print("ASSERT:FAIL undeclared write() must fail the inventory")
        return 1
    print("ASSERT:PASS verb primitive inventory refuses an undeclared write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
