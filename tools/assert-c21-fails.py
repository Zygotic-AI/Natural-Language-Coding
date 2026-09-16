#!/usr/bin/env python3
"""Known-fail fixture gate for C21 v1."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "impact-list-mismatch"
FITNESS = ROOT / "tools" / "fitness-c21.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_c21", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-c21.py")
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
    for path, gid, call in violations:
        print(f"VIOLATION {path} missing-caller {gid} {call}")
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any("apply_payment" in v[2] for v in violations):
        print("ASSERT:FAIL expected missing apply_payment")
        return 1
    print("ASSERT:PASS fixture still fails C21 v1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
