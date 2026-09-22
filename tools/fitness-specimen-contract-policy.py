#!/usr/bin/env python3
"""ADR 0006: specimen contract-change skip policy is documented and testable."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    pt = (ROOT / "tools" / "product_tree.py").read_text(encoding="utf-8", errors="replace")
    if "contract_change_applies" not in pt:
        violations.append("product_tree must define contract_change_applies")
    if "contract-change applies" not in pt:
        violations.append("product_tree must document contract-change applies opt-in")
    enf = ROOT / "docs" / "ADR-ENFORCEMENT.md"
    if enf.is_file() and "specimen" not in enf.read_text(encoding="utf-8", errors="replace").lower():
        violations.append("ADR-ENFORCEMENT should mention specimen contract policy")
    sys.path.insert(0, str(ROOT / "tools"))
    import product_tree
    from pathlib import Path as P

    green = P(ROOT / "examples" / "adopter-verify-fast-green")
    if green.is_dir() and product_tree.contract_change_applies(green):
        violations.append("adopter-verify-fast-green specimen should not apply contract_change")
    inv = P(ROOT / "examples" / "invoice-correct")
    if inv.is_dir() and not product_tree.contract_change_applies(inv):
        violations.append("invoice-correct should apply contract_change")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
