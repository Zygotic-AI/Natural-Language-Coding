"""Landmine O9a: known Gate-1 / R33 bypass fixtures must stay red (specific gates)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.field_write_bypass_fixtures.field_write_bypass_fixtures import (  # noqa: E402
    O9A_BYPASS_FIXTURE_DIRS,
)

FIELD_FITNESS = ROOT / "tools" / "fitness-no-noun-field-writes.py"
ESCAPE_FITNESS = ROOT / "tools" / "fitness-escape-hatch.py"

EXPECTATIONS: dict[str, tuple[bool, bool]] = {
    "invoice-bypass-object-setattr-violation": (True, True),
    "invoice-bypass-setattr-violation": (True, True),
    "invoice-bypass-dict-violation": (True, True),
    "invoice-bypass-multiline-violation": (True, False),
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        print(f"ASSERT:FAIL cannot load {path.name}")
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    if set(EXPECTATIONS.keys()) != set(O9A_BYPASS_FIXTURE_DIRS):
        print("ASSERT:FAIL EXPECTATIONS must match O9A_BYPASS_FIXTURE_DIRS exactly")
        return 1

    examples = ROOT / "examples"
    if examples.is_dir():
        for d in examples.iterdir():
            if not d.is_dir():
                continue
            if d.name.startswith("invoice-bypass-") and d.name not in O9A_BYPASS_FIXTURE_DIRS:
                print(f"ASSERT:FAIL unlisted invoice-bypass fixture {d.name}")
                return 1

    field_mod = load(FIELD_FITNESS, "field_fitness")
    escape_mod = load(ESCAPE_FITNESS, "escape_fitness")
    for name, (want_field, want_escape) in EXPECTATIONS.items():
        root = ROOT / "examples" / name
        if not root.is_dir():
            print(f"ASSERT:FAIL missing fixture {name}")
            return 1
        field_hits = field_mod.scan_one(root.resolve())
        escape_hits = escape_mod.scan_one(root.resolve())
        if want_field and not field_hits:
            print(f"ASSERT:FAIL {name}: Gate 1 (field-write) must fail")
            return 1
        if not want_field and field_hits:
            print(f"ASSERT:FAIL {name}: Gate 1 must not be the only miss")
            return 1
        if want_escape and not escape_hits:
            print(f"ASSERT:FAIL {name}: R33 (escape-hatch) must fail")
            return 1
        if not want_escape and escape_hits:
            print(f"ASSERT:FAIL {name}: R33 must pass (non-reflection bypass)")
            return 1

    slip = ROOT / "examples" / "invoice-bypass-landmine-unlisted-slip"
    slip.mkdir(exist_ok=True)
    try:
        extra = [
            d.name
            for d in examples.iterdir()
            if d.is_dir()
            and d.name.startswith("invoice-bypass-")
            and d.name not in O9A_BYPASS_FIXTURE_DIRS
        ]
        if not extra:
            print("ASSERT:FAIL landmine: unlisted invoice-bypass folder was not detected")
            return 1
    finally:
        slip.rmdir()

    print("ASSERT:PASS field-write bypass fixtures gate mapping")
    return 0


if __name__ == "__main__":
    sys.exit(main())
