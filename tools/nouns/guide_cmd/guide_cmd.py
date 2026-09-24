"""CLI handlers for ./nlc maintainer guide (durable .nlc/ state)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from nlc_guide_state import (
    before_generate_ok,
    end_planit,
    handoff_build,
    policy_change,
    requirements_dirty,
    start_planit,
)

BOUNDARY = "bba-emit"


def run_before_generate(root: Path, hub: Path, scopes: list[str]) -> int:
    script = hub / "tools" / "nlc-before-generate.py"
    if not script.is_file():
        script = hub / "tools" / "nlc-before-generate.py"
    argv = [sys.executable, str(script), "--repo", str(root)]
    for s in scopes:
        argv.extend(["--scope", s])
    proc = subprocess.run(argv, cwd=str(root))
    if proc.returncode != 0:
        print(
            "Knowledge check failed before generate.",
            file=sys.stderr,
        )
        print(
            "  Fix: close fact gaps in /interview, or add Assumption: with reason.",
            file=sys.stderr,
        )
        print(
            "  Agent: ./nlc maintainer guide before-generate --scope <topic>",
            file=sys.stderr,
        )
        return proc.returncode
    before_generate_ok(root, scopes)
    print("Before-generate passed. Stamp written under .nlc/")
    return 0


def dispatch_guide(args: argparse.Namespace, root: Path, hub: Path) -> int:
    cmd = args.guide_cmd
    if cmd == "planit-start":
        label = args.label or "Build & compile"
        start_planit(root, label)
        print(f"Planit session marked active: {label}")
        return 0
    if cmd == "planit-end":
        end_planit(root)
        print("Planit session cleared.")
        return 0
    if cmd == "policy-change":
        if not args.change:
            print("Missing policy change id.", file=sys.stderr)
            print(
                "  Example: ./nlc maintainer guide policy-change --change verb:Invoice.pay",
                file=sys.stderr,
            )
            return 2
        policy_change(root, args.change)
        print(f"Recorded requirement change: {args.change}")
        return 0
    if cmd == "requirements-dirty":
        requirements_dirty(root)
        print("Requirements sync flagged pending.")
        return 0
    if cmd == "handoff-build":
        handoff_build(root)
        print("Build handoff queued (pipeline-state).")
        return 0
    if cmd == "before-generate":
        scopes = args.scope or ["default"]
        return run_before_generate(root, hub, scopes)
    print(f"Unknown guide command: {cmd}", file=sys.stderr)
    return 2
