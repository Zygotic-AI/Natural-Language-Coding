#!/usr/bin/env python3
"""Known-fail: two goals import the same helper."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "imported-goal-helper"
FITNESS = ROOT / "tools" / "fitness-r15-copied-helpers.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_r15", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-r15-copied-helpers.py")
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
    for fn, _head, goals in violations:
        kind = "copied-import" if str(fn).startswith("import:") else "copied-helper"
        print(f"VIOLATION {fn} {kind} " + " ".join(goals))
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    if not any(str(v[0]).startswith("import:") and len(v[2]) >= 2 for v in violations):
        print("ASSERT:FAIL expected copied-import in two goals")
        return 1
    print("ASSERT:PASS fixture still fails R15 (imported helper)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
