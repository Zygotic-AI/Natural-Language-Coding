#!/usr/bin/env python3
"""Matrix tests for nlc_todo_ssot (negative + positive scenarios)."""

from __future__ import annotations



import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_todo_ssot import (  # noqa: E402
    SECTION_START,
    check_todo_vs_status,
    load_status,
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    base_status = load_status()
    ok_todo = (
        f"{SECTION_START}\n"
        "- ✔ **UC4 (product)** — ok @done(26-09-21 10:00)\n"
    )
    if check_todo_vs_status(ok_todo, base_status):
        violations.append("positive fixture should MET")

    bad_status = copy.deepcopy(base_status)
    bad_status["ucs"]["UC4"]["product"] = "open"
    if not check_todo_vs_status(ok_todo, bad_status):
        violations.append("negative fixture should NOT_MET when product open")

    hollow = {"schema": 1, "ucs": {}}
    if not check_todo_vs_status(ok_todo, hollow):
        violations.append("hollow status should NOT_MET")

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

