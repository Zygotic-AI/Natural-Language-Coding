#!/usr/bin/env python3
"""SSOT: TODO compiled-system @done vs integrity/uc-product-status.json."""

from __future__ import annotations



import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_todo_ssot import (  # noqa: E402
    STATUS_PATH,
    check_spine_status_vocabulary,
    check_todo_evidence_suffix,
    check_todo_vs_status,
    gate_configured,
    load_status,
)

TODO = ROOT / "TODO"
USE_CASES = ROOT / "docs" / "USE-CASES.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not STATUS_PATH.is_file():
        violations.append("missing integrity/uc-product-status.json")
    if not TODO.is_file():
        violations.append("missing TODO")
    if not USE_CASES.is_file():
        violations.append("missing docs/USE-CASES.md")
    if violations:
        for v in violations:
            print(f"VIOLATION {v}")
        print("RESULT:NOT_MET")
        return 1

    status = load_status()
    if not gate_configured(status):
        violations.append("hollow SSOT: uc-product-status.json ucs map empty")

    todo_text = TODO.read_text(encoding="utf-8", errors="replace")
    uc_text = USE_CASES.read_text(encoding="utf-8", errors="replace")

    violations.extend(check_todo_vs_status(todo_text, status))
    violations.extend(check_todo_evidence_suffix(todo_text))
    violations.extend(check_spine_status_vocabulary(uc_text))

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

