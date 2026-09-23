#!/usr/bin/env python3
"""UC4/UC5: materialize and check if/then rule IR (CLI adapter)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool
from nouns.rule_receipt.rule_receipt import check_ir, materialize_ir, write_snapshot


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="UC4/UC5 rule IR runner (v1)")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--materialize", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.materialize:
        rows = materialize_ir(root)
        path = write_snapshot(root, rows)
        print(f"rule-runner: MET materialized {path.relative_to(root)} ({len(rows)} rules)")
        return 0
    if args.check:
        errs = check_ir(root)
        if errs:
            print(errs[0], file=sys.stderr)
            print("RULE_RUNNER:NOT_MET")
            return 1
        print("RULE_RUNNER:MET")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
