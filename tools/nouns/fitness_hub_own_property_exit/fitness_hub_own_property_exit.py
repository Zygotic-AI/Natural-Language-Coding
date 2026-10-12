"""ADR 0051 SG1: hub material terminal exit must not be CI-only (R-HUB-EXIT)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "tools" / "fixtures" / "hub-own"


def main() -> int:
    """Verify hub-own property exit fixtures (direct Candidate verify)."""
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.hub_own_produce.hub_own_produce import validate_hub_material_fixture

    if not FIXTURES.is_dir():
        print(f"VIOLATION missing {FIXTURES.relative_to(ROOT)}")
        print("RESULT:NOT_MET")
        return 1
    violations: list[str] = []
    for path in sorted(FIXTURES.glob("*.json")):
        name = path.name
        data = json.loads(path.read_text(encoding="utf-8"))
        expect_hub = bool(data.pop("_expect_hub_material", False))
        expect_ok = bool(data.pop("_expect_ok_property_exit", False))
        if not expect_hub:
            continue
        ok, reason = validate_hub_material_fixture(data, "property_exit")
        if expect_ok and not ok:
            violations.append(f"{name}: expected MET got {reason}")
        if not expect_ok and ok:
            violations.append(f"{name}: expected NOT_MET got pass")
    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
