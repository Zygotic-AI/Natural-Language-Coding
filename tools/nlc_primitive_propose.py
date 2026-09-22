#!/usr/bin/env python3
"""UC12: governed primitive expansion — draft ADR before integrity/primitives.md edit."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from nlc_requirements import hub_tool

from nlc_uc_blockers import PRIMITIVE_NAMES

ROOT = Path(__file__).resolve().parents[1]


def next_adr_number(adrs: Path) -> int:
    nums: list[int] = []
    for path in adrs.glob("*.md"):
        m = re.match(r"^(\d{4})-", path.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) if nums else 0) + 1


def render_adr(num: int, name: str) -> str:
    slug = name.strip().lower().replace(" ", "-")
    return f"""# ADR {num:04d} — Add primitive `{name}`

- Status: Proposed
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (charter extension)

## Context

UC12: expand the closed primitive set only after an ADR records why `{name}` is needed.

## Decision

1. Add `{name}` to [`integrity/primitives.md`](../integrity/primitives.md) after human ratifies this ADR (Status: Accepted).
2. Prefer a new tag or fact before a new primitive when the policy can be expressed without expanding the set.

## Consequences

- Update rule IR and language scanners per ADR 0009.
- Run `./nlc maintainer rule-runner --materialize` after adoption rows reference `{name}`.

## Rejected

- Editing `primitives.md` without this ADR.
"""


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="UC12 primitive expansion ADR draft")
    parser.add_argument("--name", required=True, help="Primitive name (lowercase)")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    name = args.name.strip().lower()
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        print("primitive name must be lowercase slug", file=sys.stderr)
        return 2
    if name in PRIMITIVE_NAMES:
        print(f"primitive {name} already in closed set", file=sys.stderr)
        return 2
    root = args.root.resolve()
    adrs = root / "adrs"
    adrs.mkdir(parents=True, exist_ok=True)
    num = next_adr_number(adrs)
    path = adrs / f"{num:04d}-primitive-{name}.md"
    if path.is_file():
        print(f"exists: {path}", file=sys.stderr)
        return 2
    path.write_text(render_adr(num, name), encoding="utf-8")
    print(f"primitive-propose: MET {path.relative_to(root)} (ratify before primitives.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
