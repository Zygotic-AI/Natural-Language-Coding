#!/usr/bin/env python3
"""Known-fail: version 1 dropped a required field, no ADR."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "breaking-no-adr"
FITNESS = ROOT / "tools" / "fitness-c10.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_c10", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-c10.py")
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
    for path, ver in violations:
        print(f"VIOLATION {path} {ver}")
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any(str(v[1]).startswith("breaking:") for v in violations):
        print("ASSERT:FAIL expected breaking:")
        return 1
    print("ASSERT:PASS fixture still fails C10 (breaking, no ADR)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
