#!/usr/bin/env python3
"""Landmine ADR 0006: contract_change_blockers catches verify-impact-c21 (non-specimen)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "verify-impact-c21"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    import product_tree
    from nlc_contract_change import contract_change_blockers

    tree = FIXTURE.resolve()
    if product_tree.is_specimen(tree):
        print("ASSERT:FAIL verify-impact-c21 must not be specimen (contract path must run)")
        return 1
    blockers = contract_change_blockers(tree)
    if not blockers:
        print("ASSERT:FAIL verify-impact-c21 should contract_change_block")
        return 1
    joined = " ".join(blockers).casefold()
    if "c21" not in joined and "missing-caller" not in joined:
        print(f"ASSERT:FAIL expected C21 blocker, got {blockers}")
        return 1
    print("ASSERT:PASS contract_change_blockers on verify-impact-c21")
    return 0


if __name__ == "__main__":
    sys.exit(main())
