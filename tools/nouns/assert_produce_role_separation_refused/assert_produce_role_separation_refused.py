"""Landmine ADR 0003: produce package cannot self-audit (same producer and auditor role)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = (
    ROOT / "tools" / "fixtures" / "quality-metric" / "invalid-produce-package-self-audit.json"
)
HUB_GATE_SUBJECT = (
    ROOT / "tools" / "fixtures" / "hub-own" / "invalid-hub-own-gate-subject-same-actor.json"
)


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_produce_package import load_and_validate

    ok, kind, reason = load_and_validate(FIXTURE)
    if ok:
        print("ASSERT:FAIL self-audit produce fixture should not validate")
        return 1
    if kind != "handoff_refused":
        print(f"ASSERT:FAIL expected handoff_refused got {kind}")
        return 1
    if "ROLE_SEPARATION" not in reason:
        print(f"ASSERT:FAIL expected ROLE_SEPARATION in reason: {reason}")
        return 1
    ok2, kind2, reason2 = load_and_validate(HUB_GATE_SUBJECT)
    if ok2:
        print("ASSERT:FAIL hub gate+subject same-actor fixture should not validate")
        return 1
    if kind2 != "handoff_refused":
        print(f"ASSERT:FAIL hub gate-diff expected handoff_refused got {kind2}")
        return 1
    if "ROLE_SEPARATION" not in reason2 and "HUB_GATE_DIFF" not in reason2:
        print(f"ASSERT:FAIL expected ROLE_SEPARATION or HUB_GATE_DIFF: {reason2}")
        return 1
    print("ASSERT:PASS produce preflight refuses self-audit and hub gate+subject same actor")
    return 0


