"""Known-fail: confirmer Cx — FAIL with no rebuttal."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "confirmer-open-fail"
FITNESS = ROOT / "tools" / "fitness-c23.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_c23", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-c23.py")
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
    for path, lineno in violations:
        print(f"VIOLATION {path}:{lineno} open-finding")
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    print("ASSERT:PASS fixture still fails C23 (confirmer FAIL unrebutted)")
    return 0


