#!/usr/bin/env python3
"""Release target gates before notes, branch, or version write (ADR 0014, ADR 0022)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_migration_catalog import (  # noqa: E402
    ensure_migration_chain,
    release_target_blockers,
    upgrade_steps_toward,
)
from nlc_release_tags import last_shipped_tag, tag_version  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402


def agent_prompt(target: str, shipped_tag: str | None, blockers: list[str]) -> str:
    shipped = tag_version(shipped_tag) if shipped_tag else "?"
    lines = [
        f"Hub release v{target} is blocked (migrations / ADR 0014).",
        f"Shipped baseline: {shipped_tag or 'none'} ({shipped}) → target {target}.",
        "",
        "Gaps:",
        *[f"  - {b}" for b in blockers],
        "",
        "In your agent at repo root:",
        f"  python3 tools/nlc_release_target_preflight.py --ensure-noop --target {target}",
        "  # or: /planit ensure ADR 0014 migration chain for hub release, then re-run ./release",
        "",
        "Re-run ./release after migrations/ units exist on disk.",
    ]
    return "\n".join(lines)


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Hub release target preflight")
    parser.add_argument("--check", action="store_true", help="Exit 1 if target cannot ship")
    parser.add_argument("--target", required=True, help="Target semver (e.g. 0.2.0)")
    parser.add_argument(
        "--to",
        dest="to_ref",
        default="HEAD",
        help="Git ref for last shipped tag ancestry",
    )
    parser.add_argument(
        "--ensure-noop",
        action="store_true",
        help="Create missing noop migration.yaml units for the upgrade chain",
    )
    parser.add_argument(
        "--print-agent-prompt",
        action="store_true",
        help="On failure, print copy-paste agent instructions",
    )
    args = parser.parse_args()

    shipped_tag = last_shipped_tag(args.to_ref)
    shipped_ver = tag_version(shipped_tag) if shipped_tag else None
    if shipped_ver is None:
        print("RELEASE_TARGET:NOT_MET", file=sys.stderr)
        print("  no reachable v*.*.* tag — cannot compute shipped baseline", file=sys.stderr)
        return 1

    target = str(args.target).strip()
    print(f"RELEASE_TARGET: shipped={shipped_tag} target=v{target}")

    blockers = release_target_blockers(ROOT, target, shipped_ver)
    if blockers and args.ensure_noop:
        created = ensure_migration_chain(ROOT, shipped_ver, target)
        for path in created:
            print(f"RELEASE_TARGET:CREATED {path.relative_to(ROOT)}")
        blockers = release_target_blockers(ROOT, target, shipped_ver)

    if blockers:
        print("RELEASE_TARGET:NOT_MET", file=sys.stderr)
        for line in blockers:
            print(f"  {line}", file=sys.stderr)
        steps = upgrade_steps_toward(ROOT, shipped_ver, target)
        if steps:
            print("  required steps:", file=sys.stderr)
            for a, b in steps:
                print(f"    {a} → {b}", file=sys.stderr)
        if args.print_agent_prompt or args.ensure_noop:
            print("", file=sys.stderr)
            print(agent_prompt(target, shipped_tag, blockers), file=sys.stderr)
        return 1

    steps = upgrade_steps_toward(ROOT, shipped_ver, target)
    if steps:
        print("RELEASE_TARGET: migration chain")
        for a, b in steps:
            print(f"  {a} → {b}")
    else:
        print("RELEASE_TARGET: keep (no migration hops)")
    print("RELEASE_TARGET:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
