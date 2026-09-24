#!/usr/bin/env python3
"""P8.2: USE-CASES EXPANSION-ONLY rows align with uc-product-status expansion SSOT."""

from __future__ import annotations



import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
USE_CASES = ROOT / "docs" / "USE-CASES.md"
STATUS = ROOT / "integrity" / "uc-product-status.json"
SCOPE = ROOT / "integrity" / "product-completion-scope.json"
UC14 = ROOT / "integrity" / "uc14-product-boundary.json"


def expansion_rows(use_cases_text: str) -> list[str]:
    rows: list[str] = []
    in_needed = False
    for line in use_cases_text.splitlines():
        if line.startswith("## Needed"):
            in_needed = True
            continue
        if in_needed and line.startswith("## "):
            break
        if in_needed and "EXPANSION-ONLY" in line and "|" in line:
            rows.append(line)
    return rows


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not USE_CASES.is_file():
        violations.append("missing docs/USE-CASES.md")
    if not STATUS.is_file():
        violations.append("missing uc-product-status.json")
    if violations:
        for v in violations:
            print(f"VIOLATION {v}")
        print("RESULT:NOT_MET")
        return 1

    uc_text = USE_CASES.read_text(encoding="utf-8", errors="replace")
    rows = expansion_rows(uc_text)
    if len(rows) != 3:
        violations.append(f"USE-CASES Needed must have 3 EXPANSION-ONLY rows, got {len(rows)}")

    labels = []
    for line in rows:
        if "EXPANSION-ONLY" not in line:
            continue
        if "[UC14]" in line or "UC14" in line.split("|")[1]:
            labels.append("UC14")
        elif "[UC16]" in line or "| UC16" in line:
            labels.append("UC16")
        elif "[UC20]" in line or "| UC20" in line:
            labels.append("UC20")
    for need in ("UC14", "UC16", "UC20"):
        if need not in labels:
            violations.append(f"USE-CASES Needed missing EXPANSION-ONLY row for {need}")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    ucs = status.get("ucs") or {}
    uc4_exp = (ucs.get("UC4") or {}).get("expansion_only") or []
    uc5_exp = (ucs.get("UC5") or {}).get("expansion_only") or []
    if uc4_exp:
        violations.append("UC4 expansion_only must be empty after semantic runner v2")
    if uc5_exp:
        violations.append("UC5 expansion_only must be empty after semantic apply v2")
    if (ucs.get("UC9") or {}).get("expansion_only"):
        violations.append("UC9 expansion_only must be empty (P6.1 closed)")
    if (ucs.get("UC13") or {}).get("expansion_only"):
        violations.append("UC13 expansion_only must be empty (P6.2 closed)")
    if (ucs.get("UC14") or {}).get("expansion_only"):
        violations.append("UC14 uc-product-status expansion_only must be empty (v1 product closed)")

    if UC14.is_file():
        remain = json.loads(UC14.read_text(encoding="utf-8")).get("remain_expansion") or []
        if not remain:
            violations.append("uc14-product-boundary remain_expansion must name composable v2")

    if SCOPE.is_file():
        scope = json.loads(SCOPE.read_text(encoding="utf-8"))
        exp = scope.get("expansion_only") or {}
        for key in ("UC9.rule_tagged_blast_radius_v2", "UC13.engine_runtime_tag_strict"):
            row = exp.get(key) or {}
            if row.get("disposition") == "remain_expansion":
                violations.append(f"product-completion-scope {key} still remain_expansion")
        for key, label in (
            ("UC16.language_scanner_adapter_step2", "UC16"),
            ("UC20.per_stack_call_tree_packs", "UC20"),
        ):
            row = exp.get(key) or {}
            if row.get("disposition") != "remain_expansion":
                violations.append(f"{key} must stay remain_expansion while USE-CASES lists {label}")
        for key in ("UC4.semantic_rule_runner_adr_0007", "UC5.semantic_apply_adr_0007"):
            row = exp.get(key) or {}
            if row.get("disposition") not in ("in_reach_v2", "waive"):
                violations.append(f"{key} must be in_reach_v2 when closed")

    # Closed spine UCs must not appear as EXPANSION-ONLY Needed rows
    for closed_uc in ("UC9", "UC13"):
        if any(re.search(rf"EXPANSION-ONLY.*{closed_uc}", line) for line in rows):
            violations.append(f"USE-CASES must not EXPANSION-ONLY {closed_uc} after product close")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

