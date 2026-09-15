#!/usr/bin/env python3
"""Known-fail fixture gate for R24 v1 (adjective locality)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "invoice-locality-violation"
REQUIRED_CITATION = "goals/record-bank-payment/"
FITNESS = ROOT / "tools" / "fitness-adjective-locality.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_adjective_locality", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-adjective-locality.py")
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
    print("ASSERT:PASS fixture still fails adjective locality with required citation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
