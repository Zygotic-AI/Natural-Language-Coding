#!/usr/bin/env python3
"""Emit copy-paste remediation for hub ./release NOT_MET (ADR 0018)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_remediate import emit_release_not_met, main_purity_remediation  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    args = sys.argv[1:]
    if args[:1] == ["--print-main-purity-fixes"]:
        import argparse

        p = argparse.ArgumentParser()
        p.add_argument("--remote", default="origin")
        p.add_argument("--base", default="main")
        p.add_argument("--next-release-branch", default="")
        ns = p.parse_args(args[1:])
        root = Path(__file__).resolve().parents[1]
        for line in main_purity_remediation(
            remote=ns.remote,
            base=ns.base,
            next_release_branch=ns.next_release_branch,
            hub=root,
        ):
            print(line)
        raise SystemExit(0)

    # CLI for tests: python3 tools/nlc_release_remediate.py "problem" "gap1" "fix1"
    if len(args) < 2:
        print("usage: nlc_release_remediate.py <problem> <gap>... -- <fix>...", file=sys.stderr)
        raise SystemExit(2)
    if "--" in args:
        idx = args.index("--")
        problem = args[0]
        gaps = args[1:idx]
        fixes = args[idx + 1 :]
    else:
        problem = args[0]
        gaps = args[1:]
        fixes = []
    root = Path(__file__).resolve().parents[1]
    emit_release_not_met(problem, gaps, fixes, f"cd {root} && ./release")
    raise SystemExit(1)
