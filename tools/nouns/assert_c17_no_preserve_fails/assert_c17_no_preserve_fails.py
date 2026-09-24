"""Known-fail: verb tests have no adjective preservation."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "verb-no-preserve"
FITNESS = ROOT / "tools" / "fitness-c17.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_c17", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-c17.py")
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
    for noun, kind, name in violations:
        print(f"VIOLATION {noun} {kind} {name}")
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any(v[1] == "verb-no-preservation-test" for v in violations):
        print("ASSERT:FAIL expected verb-no-preservation-test")
        return 1
    print("ASSERT:PASS fixture still fails C17 (no preservation)")
    return 0


