#!/usr/bin/env python3
"""UC18 harness: run before PLANIT step 6 (generate).

Validates knowledge/facts.json and loads each named knowledge domain scope.

Usage:
  python3 tools/nlc-before-generate.py --repo . --scope invoice --scope pii

Output: BEFORE_GENERATE:MET or BEFORE_GENERATE:NOT_MET. Exit 0 / 1.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="NLC pre-generate knowledge domain gate")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--scope", action="append", default=[], help="Repeatable")
    args = parser.parse_args()
    repo = args.repo.resolve()
    scopes: list[str] = args.scope or ["default"]

    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate-knowledge-facts.py"), str(repo)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stdout.write(proc.stdout or "")
        sys.stderr.write(proc.stderr or "")
        print("BEFORE_GENERATE:NOT_MET validate-knowledge-facts")
        return 1

    loader = ROOT / "tools" / "load-knowledge-domain.py"
    for scope in scopes:
        lp = subprocess.run(
            [sys.executable, str(loader), scope, str(repo)],
            capture_output=True,
            text=True,
        )
        if lp.returncode != 0:
            sys.stdout.write(lp.stdout or "")
            sys.stderr.write(lp.stderr or "")
            print(f"BEFORE_GENERATE:NOT_MET load-knowledge-domain scope={scope}")
            return 1
        try:
            payload = json.loads(lp.stdout or "{}")
        except json.JSONDecodeError:
            print(f"BEFORE_GENERATE:NOT_MET bad JSON for scope={scope}")
            return 1
        print(f"KNOWLEDGE_DOMAIN scope={scope} status={payload.get('status')} facts={len(payload.get('facts') or [])}")

    print("BEFORE_GENERATE:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
