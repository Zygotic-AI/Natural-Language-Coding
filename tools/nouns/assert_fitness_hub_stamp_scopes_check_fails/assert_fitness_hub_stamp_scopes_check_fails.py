"""Landmine: fitness hub stamp scope check refuses partial stamp scopes."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.hub_stamp_scopes.hub_stamp_scopes import (  # noqa: E402
    load_scopes_file,
    stamp_scope_gap_errors,
)

FIXTURE = ROOT / "tools" / "fixtures" / "hub-stamp-scopes" / "partial-stamp-scopes.json"
SSOT = ROOT / "integrity" / "hub-stamp-scopes.json"


def main() -> int:
    required, err = load_scopes_file(SSOT)
    if err or not required:
        print("ASSERT:FAIL could not load hub SSOT scopes")
        return 1
    if not FIXTURE.is_file():
        print("ASSERT:FAIL missing partial stamp fixture")
        return 1
    stamp_scopes = json.loads(FIXTURE.read_text(encoding="utf-8")).get("scopes") or []
    if not stamp_scope_gap_errors(required, stamp_scopes):
        print("ASSERT:FAIL check must refuse partial hub stamp scopes")
        return 1
    print("ASSERT:PASS fitness check refuses partial hub stamp scopes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
