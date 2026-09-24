#!/usr/bin/env python3
"""Release context wizard (ADR 0040)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_release_resume import list_release_branches  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def commits_on_main_not_in_branch(remote: str, base: str, rel_branch: str) -> list[str]:
    proc = _git(
        "log",
        f"{remote}/{base}",
        f"^origin/{rel_branch}",
        "--oneline",
        "-n",
        "15",
    )
    if proc.returncode != 0:
        proc = _git("log", f"{remote}/{base}", f"^{rel_branch}", "--oneline", "-n", "15")
    if proc.returncode != 0:
        return []
    return [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]


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
        print("RELEASE_CONTEXT: candidate release branches:")
        for b in branches:
            print(f"  - {b}")
        return 0

    if args.branch:
        missing = commits_on_main_not_in_branch(args.remote, args.base, args.branch)
        if not missing:
            print(f"RELEASE_CONTEXT:MET {args.base} has no extra commits beyond {args.branch} (last 15 checked)")
            return 0
        print(f"RELEASE_CONTEXT:NOT_MET commits on {args.base} not in {args.branch}:", file=sys.stderr)
        for ln in missing:
            print(f"  {ln}", file=sys.stderr)
        print("  Fix: merge or cherry-pick into the release branch before shipping.", file=sys.stderr)
        return 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
