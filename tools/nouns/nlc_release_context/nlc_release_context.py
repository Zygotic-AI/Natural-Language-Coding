#!/usr/bin/env python3
"""Release context wizard (ADR 0040)."""

from __future__ import annotations

BOUNDARY = "bba-emit"


import argparse
import subprocess
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_release_resume import detect, list_release_branches  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def main_context(
    remote: str,
    base: str,
    rel_branch: str,
    git: Callable[..., subprocess.CompletedProcess[str]] = _git,
) -> tuple[str, list[str]]:
    """Return contained/not_contained/unknown for main commits absent from release."""
    proc = git(
        "rev-list",
        f"{remote}/{base}",
        f"^{rel_branch}",
    )
    if proc.returncode != 0:
        return "unknown", ["git rev-list failed"]
    commits = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    details: list[str] = []
    for commit in commits:
        parents_proc = git("rev-list", "--parents", "-n", "1", commit)
        if parents_proc.returncode != 0:
            return "unknown", [f"{commit[:12]} parent lookup failed"]
        fields = parents_proc.stdout.strip().split()
        if len(fields) < 3:
            details.append(f"{commit[:12]} is not a merge commit")
            continue
        parents = fields[1:]
        absent: list[str] = []
        for parent in parents:
            ancestor = git("merge-base", "--is-ancestor", parent, rel_branch)
            if ancestor.returncode not in (0, 1):
                return "unknown", [f"{commit[:12]} ancestry check failed"]
            if ancestor.returncode == 1:
                absent.append(parent)
        merge_tree = git("rev-parse", f"{commit}^{{tree}}")
        second_tree = git("rev-parse", f"{parents[1]}^{{tree}}")
        if merge_tree.returncode != 0 or second_tree.returncode != 0:
            return "unknown", [f"{commit[:12]} tree lookup failed"]
        merge_hex = merge_tree.stdout.strip()
        second_hex = second_tree.stdout.strip()
        # GitHub merge of the release tip: first parent is previous main (need not
        # be on the release line) and the tree equals the release parent.
        clean_release_merge = absent == [parents[0]] and merge_hex == second_hex
        if absent and not clean_release_merge:
            for parent in absent:
                details.append(
                    f"{commit[:12]} parent {parent[:12]} is absent from {rel_branch}"
                )
            continue
        if not absent and merge_hex != second_hex:
            details.append(f"{commit[:12]} has merge-only tree changes")
    if details:
        return "not_contained", details
    return "contained", []


def commits_on_main_not_in_branch(remote: str, base: str, rel_branch: str) -> list[str]:
    """Compatibility view: explanations for a context that is not contained."""
    status, details = main_context(remote, base, rel_branch)
    return [] if status == "contained" else details


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Release context checks")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    parser.add_argument("--list-branches", action="store_true")
    parser.add_argument("--branch", default="", help="release/v* to check merge completeness")
    args = parser.parse_args()

    if args.list_branches:
        branches = list_release_branches(args.remote)
        if not branches:
            print("RELEASE_CONTEXT: no release/v* branches found")
            return 0
        state = detect(args.remote, args.base)
        closed = set(state.get("closed_release_branches") or [])
        print("RELEASE_CONTEXT: candidate release branches:")
        for b in branches:
            if b in closed:
                print(f"  - {b} (shipped — closed; not an active ship target)")
            else:
                print(f"  - {b}")
        return 0

    if args.branch:
        status, details = main_context(args.remote, args.base, args.branch)
        if status == "contained":
            print(
                f"RELEASE_CONTEXT:MET {args.base} is contained by {args.branch}"
            )
            return 0
        print(
            f"RELEASE_CONTEXT:NOT_MET status={status} "
            f"{args.base} is not proven contained by {args.branch}:",
            file=sys.stderr,
        )
        for ln in details:
            print(f"  {ln}", file=sys.stderr)
        return 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
