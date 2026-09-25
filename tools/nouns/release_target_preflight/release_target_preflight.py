"""Release target gates before notes, branch, or version write (ADR 0014, ADR 0022)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from nlc_migration_catalog import (
    ensure_migration_chain,
    release_target_blockers,
    upgrade_steps_toward,
)
from nlc_release_tags import resolve_shipped_baseline, tag_is_ancestor, tag_version

BOUNDARY = "bba-emit"

HUB_ROOT = Path(__file__).resolve().parents[3]


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


def main(argv: list[str] | None = None, hub_root: Path | None = None) -> int:
    hub = (hub_root or HUB_ROOT).resolve()
    args_list = argv if argv is not None else sys.argv[1:]
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
    args = parser.parse_args(args_list)

    shipped_tag, shipped_ver = resolve_shipped_baseline(args.to_ref, hub)
    if shipped_tag and not tag_is_ancestor(shipped_tag, args.to_ref, hub):
        print(
            f"RELEASE_TARGET: {shipped_tag} is not an ancestor of {args.to_ref}; "
            "using tag semver for ADR 0014 migration baseline only",
            file=sys.stderr,
        )
    if shipped_ver is None:
        print("RELEASE_TARGET:NOT_MET", file=sys.stderr)
        print("  no v*.*.* tag in repo — cannot compute shipped baseline", file=sys.stderr)
        return 1

    target = str(args.target).strip()
    print(f"RELEASE_TARGET: shipped={shipped_tag} target=v{target}")

    blockers = release_target_blockers(hub, target, shipped_ver)
    if blockers and args.ensure_noop:
        created = ensure_migration_chain(hub, shipped_ver, target)
        for path in created:
            print(f"RELEASE_TARGET:CREATED {path.relative_to(hub)}")
        blockers = release_target_blockers(hub, target, shipped_ver)

    if blockers:
        print("RELEASE_TARGET:NOT_MET", file=sys.stderr)
        for line in blockers:
            print(f"  {line}", file=sys.stderr)
        steps = upgrade_steps_toward(hub, shipped_ver, target)
        if steps:
            print("  required steps:", file=sys.stderr)
            for a, b in steps:
                print(f"    {a} → {b}", file=sys.stderr)
        if args.print_agent_prompt or args.ensure_noop:
            print("", file=sys.stderr)
            print(agent_prompt(target, shipped_tag, blockers), file=sys.stderr)
        return 1

    steps = upgrade_steps_toward(hub, shipped_ver, target)
    if steps:
        print("RELEASE_TARGET: migration chain")
        for a, b in steps:
            print(f"  {a} → {b}")
    else:
        print("RELEASE_TARGET: keep (no migration hops)")
    print("RELEASE_TARGET:MET")
    return 0
