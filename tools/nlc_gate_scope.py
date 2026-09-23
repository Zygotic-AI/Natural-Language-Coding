#!/usr/bin/env python3
"""ADR 0010: declare Planit-generated artifacts that require gate receipts (CLI adapter)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.gate_ledger.gate_ledger import (  # noqa: E402
    SCOPE_FILE,
    add_scope_path,
    load_scope_paths,
    scoped_artifact_paths,
)

__all__ = [
    "SCOPE_FILE",
    "add_scope_path",
    "load_scope_paths",
    "scoped_artifact_paths",
]


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Declare ADR 0010 gate-scoped artifacts")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--add", dest="artifact", help="Repo-relative artifact path")
    parser.add_argument("--list", action="store_true", help="Print scoped paths")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.list:
        for rel in load_scope_paths(root):
            print(rel)
        return 0
    if not args.artifact:
        print("gate-scope needs --add <path> or --list", file=sys.stderr)
        return 2
    try:
        add_scope_path(root, args.artifact)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"gate-scope: MET artifact={args.artifact}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
