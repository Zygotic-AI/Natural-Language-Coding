"""Known-fail fixture gate for R13 v1 (one entrypoint per goal)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "extra-goal-entrypoint"
FITNESS = ROOT / "tools" / "fitness-r13-entrypoints.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_r13", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-r13-entrypoints.py")
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
    for goal, entries in violations:
        print(f"VIOLATION {goal} extra-entrypoint " + " ".join(entries))
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    names = {n for _, ents in violations for n in ents}
    if not {"implementation.py", "run.py"} <= names:
        print("ASSERT:FAIL expected implementation.py and run.py")
        return 1
    print("ASSERT:PASS fixture still fails R13 v1")
    return 0


