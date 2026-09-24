"""Known-fail fixture gate for contract-presence v1."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "missing-contract"
FITNESS = ROOT / "tools" / "fitness-contract-presence.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_contract_presence", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-contract-presence.py")
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
    for path, kind in violations:
        print(f"VIOLATION {path} {kind}")
    kinds = {k for _, k in violations}
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    need = {"missing-goal-input", "missing-goal-output", "missing-noun-verbs-schema"}
    if not need <= kinds:
        print(f"ASSERT:FAIL missing kinds {sorted(need - kinds)}")
        return 1
    print("ASSERT:PASS fixture still fails contract-presence v1")
    return 0


