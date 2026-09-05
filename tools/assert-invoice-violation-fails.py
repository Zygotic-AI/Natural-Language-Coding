#!/usr/bin/env python3
"""Known-fail fixture gate for fitness check 1.

Runs check 1 on examples/invoice-violation/ only.

Input: no argv. Fixed scan tree: examples/invoice-violation/
  (via fitness scan_one on that root).

Output: fitness `VIOLATION …` lines when present, then `RESULT:MET|NOT_MET`,
  then one of:
  ASSERT:PASS fixture still fails check 1 with required citation
  ASSERT:FAIL … (missing fixture / clean fixture / missing citation / load error)

Failure mode: process exit 0 = ASSERT:PASS (fixture still NOT_MET with
  goals/record-bank-payment/ citation); exit 1 = ASSERT:FAIL.
  Does not swallow exceptions silently — unexpected errors propagate and abort.
  (Load failure prints ASSERT:FAIL and exits 1.)
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "invoice-violation"
REQUIRED_CITATION = "goals/record-bank-payment/"
FITNESS = ROOT / "tools" / "fitness-no-noun-field-writes.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location(
        "fitness_no_noun_field_writes", FITNESS
    )
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-no-noun-field-writes.py")
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
    for path, lineno, field in violations:
        print(f"VIOLATION {path}:{lineno} {field}")
    cited = [
        (path, lineno, field)
        for path, lineno, field in violations
        if REQUIRED_CITATION in path.replace("\\", "/")
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
    print("ASSERT:PASS fixture still fails check 1 with required citation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
