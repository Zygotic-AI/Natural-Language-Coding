#!/usr/bin/env python3
"""Landmine ADR 0014: hub version must sit on a complete migration catalog."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_migration_catalog import migration_catalog_blockers

    blockers = migration_catalog_blockers(ROOT)
    if blockers:
        print("ASSERT:FAIL migration catalog")
        for b in blockers:
            print(f"  {b}")
        return 1
    print("ASSERT:PASS migration catalog complete for hub version")
    return 0


if __name__ == "__main__":
    sys.exit(main())
