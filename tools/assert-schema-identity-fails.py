#!/usr/bin/env python3
"""Known-fail fixture gate for R11/C9 v1."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "schema-identity-violation"
FITNESS = ROOT / "tools" / "fitness-schema-identity.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_schema_identity", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-schema-identity.py")
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
    for name, types, paths in violations:
        print(f"VIOLATION {name} types={','.join(types)} " + " ".join(paths))
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    names = {v[0] for v in violations}
    if "amount" not in names:
        print("ASSERT:FAIL expected a fork on field name amount")
        return 1
    print("ASSERT:PASS fixture still fails schema-identity v1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
