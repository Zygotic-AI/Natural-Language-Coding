"""Known-fail fixture gate for R25 v1."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "noun-without-tests"
FITNESS = ROOT / "tools" / "fitness-r25-noun-tests.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_r25", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-r25-noun-tests.py")
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    if not FIXTURE.is_dir():
        print(f"ASSERT:FAIL missing fixture {FIXTURE.relative_to(ROOT)}")
        return 1
    fitness = load_fitness()
    missing = fitness.scan_one(FIXTURE.resolve())
    for noun in missing:
        print(f"VIOLATION {noun} missing-noun-tests")
    if not missing:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any("invoice" in n for n in missing):
        print("ASSERT:FAIL expected invoice noun")
        return 1
    print("ASSERT:PASS fixture still fails R25 v1")
    return 0


