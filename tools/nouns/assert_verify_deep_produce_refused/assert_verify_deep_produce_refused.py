"""Landmine: verify-deep extra blockers refuse incomplete produce package."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPECIMEN = ROOT / "examples" / "verify-produce-handoff"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_deep_extra_blockers

    if not SPECIMEN.is_dir():
        print(f"ASSERT:FAIL missing {SPECIMEN.relative_to(ROOT)}")
        return 1
    reasons = verify_deep_extra_blockers(SPECIMEN.resolve())
    if not reasons:
        print("ASSERT:FAIL verify-deep extra should block incomplete produce package")
        return 1
    combined = " ".join(reasons).lower()
    if "produce" not in combined and "ssot" not in combined:
        print(f"ASSERT:FAIL unexpected blockers: {reasons}")
        return 1
    print("ASSERT:PASS verify-deep extra refuses verify-produce-handoff")
    return 0


