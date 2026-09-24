"""Known-fail fixture gate for C15 v2 missing idempotency key at the call."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "retrying-no-key"
FITNESS = ROOT / "tools" / "fitness-c15-idempotent.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_c15", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-c15-idempotent.py")
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
    for path, kind, verb in violations:
        print(f"VIOLATION {path} {kind} {verb}")
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any(v[1] == "missing-idempotency-key" and v[2] == "apply_payment" for v in violations):
        print("ASSERT:FAIL expected missing-idempotency-key apply_payment")
        return 1
    print("ASSERT:PASS fixture still fails C15 (missing-idempotency-key)")
    return 0


