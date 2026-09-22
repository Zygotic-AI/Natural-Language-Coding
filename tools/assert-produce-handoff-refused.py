#!/usr/bin/env python3
"""Landmine ADR 0004/0005: produce package without SSOT evidence must handoff_refused."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tools" / "fixtures" / "quality-metric" / "invalid-produce-package-no-evidence.json"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_produce_package import load_and_validate

    ok, kind, reason = load_and_validate(FIXTURE)
    if ok:
        print("ASSERT:FAIL invalid produce fixture should not validate")
        return 1
    if kind != "handoff_refused":
        print(f"ASSERT:FAIL expected handoff_refused got {kind}: {reason}")
        return 1
    if "SSOT_EXIT_EVIDENCE" not in reason and "quality_evidence" not in reason:
        print(f"ASSERT:FAIL unexpected reason: {reason}")
        return 1
    print("ASSERT:PASS produce preflight refuses missing evidence/SSOT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
