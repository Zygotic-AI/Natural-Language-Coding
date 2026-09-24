"""Landmine ADR 0003: verify-deep extra refuses self-audit produce package."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPECIMEN = ROOT / "examples" / "verify-produce-self-audit"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_deep_extra_blockers

    reasons = verify_deep_extra_blockers(SPECIMEN.resolve())
    if not reasons:
        print("ASSERT:FAIL verify-deep extra should block self-audit produce package")
        return 1
    combined = " ".join(reasons)
    if "ROLE_SEPARATION" not in combined:
        print(f"ASSERT:FAIL expected ROLE_SEPARATION: {reasons}")
        return 1
    print("ASSERT:PASS verify-deep extra refuses verify-produce-self-audit")
    return 0


