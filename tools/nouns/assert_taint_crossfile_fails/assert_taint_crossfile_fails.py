"""Known-fail: taint returned through a helper in another file."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "card-taint-crossfile"
FITNESS = ROOT / "tools" / "fitness-taint-lifetime.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_taint", FITNESS)
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
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean")
        return 1
    print("RESULT:NOT_MET")
    cited = [v for v in violations if "implementation.py" in v[0] and "return-taint" in v[2]]
    if not cited:
        print("ASSERT:FAIL expected return-taint on implementation.py")
        return 1
    print("ASSERT:PASS fixture still fails R32 (cross-file helper)")
    return 0


