"""Prove hub in-force exclusion prefixes skip docs/rca and docs/history."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.hub_in_force_surfaces.hub_in_force_surfaces import (  # noqa: E402
    is_excluded,
    iter_in_force_files,
)


def main() -> int:
    for must_exclude in (
        "docs/rca/2026-09-01-example.md",
        "docs/history/foo.md",
        "examples/internal-link-landmine/broken.md",
    ):
        if not is_excluded(must_exclude):
            print(f"ASSERT:FAIL expected excluded {must_exclude!r}")
            return 1
    in_force = iter_in_force_files(ROOT, suffixes=(".md",))
    rca_hits = [p for p in in_force if "docs/rca/" in p.relative_to(ROOT).as_posix()]
    if rca_hits:
        print(f"ASSERT:FAIL docs/rca still in-force scan: {rca_hits[0]}")
        return 1
    agents = ROOT / "AGENTS.md"
    if agents not in in_force:
        print("ASSERT:FAIL AGENTS.md must be in-force")
        return 1
    print("ASSERT:PASS hub in-force exclusions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
