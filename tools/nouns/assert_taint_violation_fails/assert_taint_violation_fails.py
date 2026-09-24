"""Known-fail fixture gate for A5 v1 (taint lifetime)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "card-taint-violation"
REQUIRED_CITATION = "goals/print-receipt/"
FITNESS = ROOT / "tools" / "fitness-taint-lifetime.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_taint_lifetime", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-taint-lifetime.py")
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
    for path, lineno, kind in violations:
        print(f"VIOLATION {path}:{lineno} {kind}")
    cited = [v for v in violations if REQUIRED_CITATION in v[0].replace("\\", "/")]
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean (checker dead or example fixed)")
        return 1
    print("RESULT:NOT_MET")
    if not cited:
        print(f"ASSERT:FAIL NOT_MET but no VIOLATION cites {REQUIRED_CITATION}")
        return 1
    print("ASSERT:PASS fixture still fails taint lifetime with required citation")
    return 0


