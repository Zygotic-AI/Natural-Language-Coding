#!/usr/bin/env python3
"""P5.5 x4-t1-other-or-lib: inventory + noun pilot progress (default-closed)."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / "integrity" / "hub-x4-tranche-plan.json"
REMAINDER = ROOT / "integrity" / "hub-x4-remainder.json"
TRANCHE_ID = "x4-t1-other-or-lib"


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
    progress = plan.get("tranche_1_progress") or {}
    baseline = progress.get("baseline_other_or_lib")
    floor = progress.get("floor_other_or_lib")
    required_nouns = list(progress.get("converted_lib_nouns") or [])
    if baseline is None or floor is None or not required_nouns:
        violations.append("tranche_1_progress needs baseline_other_or_lib, floor_other_or_lib, converted_lib_nouns")

    if not REMAINDER.is_file():
        violations.append("missing hub-x4-remainder.json")
        return _finish(violations)

    inv = json.loads(REMAINDER.read_text(encoding="utf-8"))
    counts = inv.get("counts") or {}
    other = counts.get("other_or_lib")
    emit_open = counts.get("emit_path_open")
    if emit_open != 0:
        violations.append(f"emit_path_open must be 0 got {emit_open}")
    if inv.get("emit_path_open"):
        violations.append("emit_path_open list must be empty")

    entries = inv.get("entries") or []
    class_other = sum(1 for e in entries if e.get("class") == "other-or-lib")
    if other is not None and class_other != other:
        violations.append(f"counts.other_or_lib {other} != entries other-or-lib {class_other}")
    if baseline is not None and other is not None and other > baseline:
        violations.append(f"other_or_lib {other} above baseline {baseline}")
    if floor is not None and other is not None and other > floor:
        violations.append(f"other_or_lib {other} still above tranche floor {floor}")

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

