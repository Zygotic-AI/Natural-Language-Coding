"""Landmine ADR 0006: teaching adopter invoice-correct has no contract_change blockers."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "invoice-correct"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    import product_tree
    from nlc_contract_change import contract_change_blockers

    tree = FIXTURE.resolve()
    if product_tree.is_specimen(tree):
        print("ASSERT:FAIL invoice-correct must not be a specimen (contract checks apply)")
        return 1
    blockers = contract_change_blockers(tree)
    if blockers:
        print("ASSERT:FAIL invoice-correct should MET contract_change_blockers")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS invoice-correct clear contract_change blockers")
    return 0


