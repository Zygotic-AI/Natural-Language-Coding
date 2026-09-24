"""Known-fail fixture gate for R15 v1."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "copied-goal-helper"
FITNESS = ROOT / "tools" / "fitness-r15-copied-helpers.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_r15", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-r15-copied-helpers.py")
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    if not FIXTURE.is_dir():
        print(f"ASSERT:FAIL missing fixture {FIXTURE.relative_to(ROOT)}")
        return 1
    fitness = load_fitness()
    violations = fitness.scan_one(FIXTURE.resolve())
    for fn, _head, goals in violations:
        print(f"VIOLATION {fn} copied-helper " + " ".join(goals))
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any("next_id" in v[0] and len(v[2]) >= 2 for v in violations):
        print("ASSERT:FAIL expected next_id in two goals")
        return 1
    print("ASSERT:PASS fixture still fails R15 v1")
    return 0


