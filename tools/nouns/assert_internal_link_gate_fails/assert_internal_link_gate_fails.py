"""Landmine: fitness-internal-links must fail on a deliberate broken relative link."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "internal-link-landmine" / "broken.md"
FITNESS = ROOT / "tools" / "nouns" / "fitness_internal_links" / "fitness_internal_links.py"


def load_module():
    spec = importlib.util.spec_from_file_location("fitness_internal_links", FITNESS)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load fitness_internal_links")
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    if not FIXTURE.is_file():
        print(f"ASSERT:FAIL missing fixture {FIXTURE.relative_to(ROOT)}")
        return 1
    mod = load_module()
    hits = mod.scan_file(FIXTURE)
    if not hits:
        print("ASSERT:FAIL fitness-internal-links did not detect broken link")
        return 1
    print("ASSERT:PASS fitness-internal-links detects broken relative links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
