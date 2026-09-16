#!/usr/bin/env python3
"""Known-fail fixture gate for C24 v1."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
    for path in missing:
        print(f"VIOLATION {path} missing-ratification")
    if not missing:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    print("ASSERT:PASS fixture still fails C24 v1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
