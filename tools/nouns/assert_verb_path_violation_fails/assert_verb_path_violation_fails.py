"""Known-fail fixture gate for R6/C5 v1 (persistence escapes).

Runs fitness-verb-path.py on examples/invoice-verb-path-violation/ only.

Input: no argv.
Output: VIOLATION lines, RESULT:MET|NOT_MET, ASSERT:PASS or ASSERT:FAIL.
Failure mode: exit 0 = ASSERT:PASS; exit 1 = ASSERT:FAIL.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "invoice-verb-path-violation"
REQUIRED_CITATION = "goals/record-bank-payment/"
FITNESS = ROOT / "tools" / "fitness-verb-path.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_verb_path", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-verb-path.py")
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
    cited = [
        item
        for item in violations
        if REQUIRED_CITATION in item[0].replace("\\", "/")
    ]
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean (checker dead or example fixed)")
        return 1
    print("RESULT:NOT_MET")
    if not cited:
        print(
            "ASSERT:FAIL NOT_MET but no VIOLATION cites "
            f"{REQUIRED_CITATION}"
        )
        return 1
    print("ASSERT:PASS fixture still fails verb-path v1 with required citation")
    return 0


