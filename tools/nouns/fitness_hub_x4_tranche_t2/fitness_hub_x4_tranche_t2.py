#!/usr/bin/env python3
"""P5.6 x4-t2-assert-batch-a: inventory + assert noun pilot progress (default-closed)."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / "integrity" / "hub-x4-tranche-plan.json"
REMAINDER = ROOT / "integrity" / "hub-x4-remainder.json"
TRANCHE_ID = "x4-t2-assert-batch-a"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not PLAN.is_file():
        violations.append("missing hub-x4-tranche-plan.json")
        return _finish(violations)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    tranche = next((t for t in plan.get("tranches") or [] if t.get("id") == TRANCHE_ID), None)
    if tranche is None:
        violations.append(f"tranche plan missing id {TRANCHE_ID}")
    progress = plan.get("tranche_2_progress") or {}
    baseline = progress.get("baseline_assert_only")
    floor = progress.get("floor_assert_only")
    required_nouns = list(progress.get("converted_assert_nouns") or [])
    if baseline is None or floor is None or not required_nouns:
        violations.append(
            "tranche_2_progress needs baseline_assert_only, floor_assert_only, converted_assert_nouns"
        )

    if not REMAINDER.is_file():
        violations.append("missing hub-x4-remainder.json")
        return _finish(violations)

    inv = json.loads(REMAINDER.read_text(encoding="utf-8"))
    counts = inv.get("counts") or {}
    assert_only = counts.get("assert_only")
    emit_open = counts.get("emit_path_open")
    other = counts.get("other_or_lib")
    if emit_open != 0:
        violations.append(f"emit_path_open must be 0 got {emit_open}")
    if other != 0:
        violations.append(f"other_or_lib must stay 0 got {other}")
    if inv.get("emit_path_open"):
        violations.append("emit_path_open list must be empty")

    entries = inv.get("entries") or []
    class_assert = sum(1 for e in entries if e.get("class") == "assert-only")
    if assert_only is not None and class_assert != assert_only:
        violations.append(f"counts.assert_only {assert_only} != entries assert-only {class_assert}")
    if baseline is not None and assert_only is not None and assert_only > baseline:
        violations.append(f"assert_only {assert_only} above baseline {baseline}")
    if floor is not None and assert_only is not None and assert_only > floor:
        violations.append(f"assert_only {assert_only} still above tranche floor {floor}")

    pilots = {p.get("noun"): p for p in inv.get("noun_pilots") or []}
    for noun in required_nouns:
        if noun not in pilots:
            violations.append(f"noun_pilots missing {noun}")

    if subprocess.run(
        [sys.executable, str(ROOT / "tools" / "fitness-hub-x4-noun-pilot.py")],
        cwd=str(ROOT),
        check=False,
    ).returncode != 0:
        violations.append("fitness-hub-x4-noun-pilot.py must MET")

    return _finish(violations)


def _finish(violations: list[str]) -> int:
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

