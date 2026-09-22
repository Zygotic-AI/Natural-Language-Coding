#!/usr/bin/env python3
"""JOBS-TO-BE-DONE Blocked/Available vs uc-product-status + TODO."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_todo_ssot import STATUS_PATH, check_jobs_vs_status, load_status  # noqa: E402

JOBS = ROOT / "docs" / "JOBS-TO-BE-DONE.md"
TODO = ROOT / "TODO"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not JOBS.is_file():
        violations.append("missing JOBS-TO-BE-DONE.md")
    if not STATUS_PATH.is_file():
        violations.append("missing uc-product-status.json")
    if violations:
        for v in violations:
            print(f"VIOLATION {v}")
        print("RESULT:NOT_MET")
        return 1
    status = load_status()
    jobs = JOBS.read_text(encoding="utf-8", errors="replace")
    todo = TODO.read_text(encoding="utf-8", errors="replace") if TODO.is_file() else ""
    violations.extend(check_jobs_vs_status(jobs, status, todo))
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
