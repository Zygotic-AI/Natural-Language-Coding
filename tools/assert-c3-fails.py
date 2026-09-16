#!/usr/bin/env python3
"""Known-fail fixture gate for C3 / R3 v1."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "orchestration-on-noun"
FITNESS = ROOT / "tools" / "fitness-c3.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_c3", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-c3.py")
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
    for path, verb, owner in violations:
        print(f"VIOLATION {path} cross-noun {verb} owned-by {owner}")
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any(v[1] == "apply_payment" and v[2] == "invoice" for v in violations):
        print("ASSERT:FAIL expected apply_payment owned-by invoice")
        return 1
    print("ASSERT:PASS fixture still fails C3 v1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
