#!/usr/bin/env python3
"""Known-fail: verb mentions fields in a string, never reads/writes them."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "mention-only-verb"
FITNESS = ROOT / "tools" / "fitness-r4.py"


def load_fitness():
    spec = importlib.util.spec_from_file_location("fitness_r4", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness-r4.py")
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
    for path, name in violations:
        print(f"VIOLATION {path} stray-verb {name}")
    if not violations:
        print("RESULT:MET")
        print("ASSERT:FAIL fixture is clean (string mention counted as use)")
        return 1
    print("RESULT:NOT_MET")
    if not any(v[1] == "export_csv" for v in violations):
        print("ASSERT:FAIL expected export_csv")
        return 1
    print("ASSERT:PASS fixture still fails R4 (mention-only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
