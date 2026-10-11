"""Landmine ADR 0004/0005: produce package without SSOT evidence must handoff_refused."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "tools" / "fixtures" / "quality-metric" / "invalid-produce-package-no-evidence.json"
HUB_CI_ONLY = ROOT / "tools" / "fixtures" / "hub-own" / "invalid-hub-own-ci-only-exit.json"


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
    ok2, kind2, reason2 = load_and_validate(HUB_CI_ONLY)
    if ok2:
        print("ASSERT:FAIL hub CI-only exit fixture should not validate")
        return 1
    if kind2 != "handoff_refused":
        print(f"ASSERT:FAIL hub profile expected handoff_refused got {kind2}: {reason2}")
        return 1
    if "R-HUB-EXIT" not in reason2:
        print(f"ASSERT:FAIL expected R-HUB-EXIT in reason: {reason2}")
        return 1
    print("ASSERT:PASS produce preflight refuses missing evidence/SSOT and hub CI-only exit")
    return 0


