#!/usr/bin/env python3
"""P5.7 x4-t3-assert-batch-b: all assert landmines noun-backed (default-closed)."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / "integrity" / "hub-x4-tranche-plan.json"
REMAINDER = ROOT / "integrity" / "hub-x4-remainder.json"
TRANCHE_ID = "x4-t3-assert-batch-b"


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
    progress = plan.get("tranche_3_progress") or {}
    target = progress.get("target_assert_only")
    if target is None:
        violations.append("tranche_3_progress needs target_assert_only")

    if not REMAINDER.is_file():
        violations.append("missing hub-x4-remainder.json")
        return _finish(violations)

    inv = json.loads(REMAINDER.read_text(encoding="utf-8"))
    counts = inv.get("counts") or {}
    assert_only = counts.get("assert_only")
    emit_open = counts.get("emit_path_open")
    other = counts.get("other_or_lib")
    backed = counts.get("noun_backed_assert")

    if emit_open != 0:
        violations.append(f"emit_path_open must be 0 got {emit_open}")
    if other != 0:
        violations.append(f"other_or_lib must stay 0 got {other}")
    if inv.get("emit_path_open"):
        violations.append("emit_path_open list must be empty")
    if not inv.get("assert_tranche_complete"):
        violations.append("hub-x4-remainder assert_tranche_complete must be true")

    entries = inv.get("entries") or []
    class_assert = sum(1 for e in entries if e.get("class") == "assert-only")
    if assert_only != 0 or class_assert != 0:
        violations.append(f"assert_only must be 0 got counts={assert_only} entries={class_assert}")
    if target is not None and assert_only is not None and assert_only != target:
        violations.append(f"assert_only {assert_only} != target {target}")
    disk_asserts = len(list((ROOT / "tools").glob("assert-*.py")))
    if backed is not None and backed < disk_asserts:
        violations.append(f"noun_backed_assert {backed} expected >= disk assert tools {disk_asserts}")

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

