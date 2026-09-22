#!/usr/bin/env python3
"""ADR 0021/0006: verify pipeline wires compliance blockers in order."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPLIANCE = ROOT / "tools" / "nlc_compliance.py"
VERIFY = ROOT / "tools" / "nlc_verify.py"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not COMPLIANCE.is_file():
        violations.append("missing nlc_compliance.py")
    else:
        c = COMPLIANCE.read_text(encoding="utf-8", errors="replace")
        for fn in (
            "rule_coverage_blockers",
            "gate_record_blockers",
            "before_generate_stamp_blockers",
        ):
            if f"def {fn}" not in c:
                violations.append(f"nlc_compliance missing {fn}")
        if "from nlc_contract_change import contract_change_blockers" not in c:
            violations.append("verify_fast_blockers must import contract_change_blockers")
        if "contract_change_blockers(root)" not in c:
            violations.append("verify_fast_blockers must call contract_change_blockers")
    if not VERIFY.is_file():
        violations.append("missing nlc_verify.py")
    else:
        v = VERIFY.read_text(encoding="utf-8", errors="replace")
        if "verify_fast_blockers(root)" not in v:
            violations.append("nlc_verify pipeline must call verify_fast_blockers")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
