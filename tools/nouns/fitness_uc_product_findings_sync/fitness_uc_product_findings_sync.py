#!/usr/bin/env python3
"""Refuse uc-product-status.json disagreeing with FINDINGS expansion narrative (O10)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = ROOT / "FINDINGS.md"
STATUS = ROOT / "integrity" / "uc-product-status.json"

# expansion_only keys FINDINGS Parked rows require in uc-product-status.
SCOPE_EXPANSION_KEYS: tuple[str, ...] = (
    "UC4.semantic_rule_runner_adr_0007",
    "UC5.semantic_apply_adr_0007",
    "UC14.composable_ir_cross_primitive",
    "UC16.language_scanner_adapter_step2",
    "UC20.per_stack_call_tree_packs",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not FINDINGS.is_file() or not STATUS.is_file():
        violations.append("missing FINDINGS.md or uc-product-status.json")
    else:
        findings = FINDINGS.read_text(encoding="utf-8", errors="replace")
        status = json.loads(STATUS.read_text(encoding="utf-8"))
        ucs = status.get("ucs") or {}

        if "semantic" not in findings or "0042" not in findings:
            violations.append("FINDINGS must state UC4/UC5 semantic expansion per ADR 0042")
        if "composable" not in findings:
            violations.append("FINDINGS must document UC14 composable IR expansion")

        all_exp: set[str] = set()
        for block in ucs.values():
            all_exp.update(block.get("expansion_only") or [])
        for key in SCOPE_EXPANSION_KEYS:
            if key not in all_exp:
                violations.append(f"uc-product-status expansion_only missing {key!r} (FINDINGS parked expansion)")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
