#!/usr/bin/env python3
"""Landmine: adopter-verify-fast-green has no verify_fast_blockers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "adopter-verify-fast-green"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers
    from nlc_verify import pipeline_blockers, verify_fast, verified_path

    root = FIXTURE.resolve()
    blockers = verify_fast_blockers(root)
    if blockers:
        print("ASSERT:FAIL verify_fast_blockers should be empty")
        for b in blockers:
            print(f"  {b}")
        return 1
    pipeline = pipeline_blockers(root)
    if pipeline:
        print("ASSERT:FAIL pipeline_blockers should be empty (requirements/regen)")
        for b in pipeline:
            print(f"  {b}")
        return 1
    if not verified_path(root).is_file():
        print("ASSERT:FAIL missing .nlc/verified.json — run verify-deep on specimen")
        return 1
    ok, reasons = verify_fast(root)
    if not ok:
        print("ASSERT:FAIL ./nlc verify fast path should MET")
        for r in reasons:
            print(f"  {r}")
        return 1
    print("ASSERT:PASS adopter-verify-fast-green verify_fast MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
