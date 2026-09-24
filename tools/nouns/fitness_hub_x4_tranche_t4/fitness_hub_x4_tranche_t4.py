#!/usr/bin/env python3
"""P5.8 x4-t4-fitness-batch: all fitness-*.py noun-backed (default-closed)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / "integrity" / "hub-x4-tranche-plan.json"
REMAINDER = ROOT / "integrity" / "hub-x4-remainder.json"
TRANCHE_ID = "x4-t4-fitness-complete"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not PLAN.is_file():
        violations.append("missing hub-x4-tranche-plan.json")
    else:
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
        if not any(t.get("id") == TRANCHE_ID for t in plan.get("tranches") or []):
            violations.append(f"tranche plan missing id {TRANCHE_ID}")
        progress = plan.get("tranche_4_progress") or {}
        if progress.get("target_fitness_only") != 0:
            violations.append("tranche_4_progress.target_fitness_only must be 0")

    if not REMAINDER.is_file():
        violations.append("missing hub-x4-remainder.json")
        return _finish(violations)

    inv = json.loads(REMAINDER.read_text(encoding="utf-8"))
    counts = inv.get("counts") or {}
    fitness_only = counts.get("fitness_only")
    backed = counts.get("noun_backed_fitness")
    if not inv.get("fitness_tranche_complete"):
        violations.append("hub-x4-remainder fitness_tranche_complete must be true")
    if fitness_only != 0:
        violations.append(f"fitness_only must be 0 got {fitness_only}")
    disk_fitness = len(list((ROOT / "tools").glob("fitness-*.py")))
    if backed is not None and backed < disk_fitness:
        violations.append(f"noun_backed_fitness {backed} expected >= disk fitness tools {disk_fitness}")

    class_fit = sum(1 for e in inv.get("entries") or [] if e.get("class") == "fitness-only")
    if class_fit != 0:
        violations.append(f"entries fitness-only class count {class_fit}")

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

