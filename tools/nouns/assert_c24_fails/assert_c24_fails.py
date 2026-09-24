"""Known-fail fixture gate for C24 v1."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "unsigned-class-a"

FITNESS = ROOT / "tools" / "fitness-c24.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_c24", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-c24.py")
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
    for path, kind in missing:
        print(f"VIOLATION {path} {kind}")
    if not missing:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any(v[1] == "missing-ratification" for v in missing):
        print("ASSERT:FAIL expected missing-ratification")
        return 1
    print("ASSERT:PASS fixture still fails C24 (missing-ratification)")

    return 0


