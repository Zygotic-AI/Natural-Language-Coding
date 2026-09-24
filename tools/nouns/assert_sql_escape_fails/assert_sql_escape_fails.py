"""Known-fail: SQL execute in a goal."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "sql-escape-hatch"
FITNESS = ROOT / "tools" / "fitness-escape-hatch.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_escape", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-escape-hatch.py")
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
    for path, lineno, kind in violations:
        print(f"VIOLATION {path}:{lineno} {kind}")
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any(v[2] == "sql-hatch" for v in violations):
        print("ASSERT:FAIL expected sql-hatch")
        return 1
    print("ASSERT:PASS fixture still fails R33 (sql-hatch)")
    return 0


