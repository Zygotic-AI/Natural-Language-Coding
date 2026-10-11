"""Landmine O9a: known Gate-1 / R33 bypass fixtures must stay red."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = (
    "invoice-bypass-object-setattr-violation",
    "invoice-bypass-setattr-violation",
    "invoice-bypass-dict-violation",
    "invoice-bypass-multiline-violation",
)
FIELD_FITNESS = ROOT / "tools" / "fitness-no-noun-field-writes.py"
ESCAPE_FITNESS = ROOT / "tools" / "fitness-escape-hatch.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        print(f"ASSERT:FAIL cannot load {path.name}")
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    field_mod = load(FIELD_FITNESS, "field_fitness")
    escape_mod = load(ESCAPE_FITNESS, "escape_fitness")
    for name in FIXTURES:
        root = ROOT / "examples" / name
        if not root.is_dir():
            print(f"ASSERT:FAIL missing fixture {name}")
            return 1
        field_hits = field_mod.scan_one(root.resolve())
        escape_hits = escape_mod.scan_one(root.resolve())
        if not field_hits and not escape_hits:
            print(f"ASSERT:FAIL fixture {name} is clean (bypass not detected)")
            return 1
    print("ASSERT:PASS field-write bypass fixtures still fail Gate 1 / R33")
    return 0


if __name__ == "__main__":
    sys.exit(main())
