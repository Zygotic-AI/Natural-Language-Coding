#!/usr/bin/env python3
"""Record PLANIT 6.5 gate PASS for an artifact (ADR 0010) — CLI adapter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.gate_ledger.gate_ledger import append_record  # noqa: E402

__all__ = ["append_record"]


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(
        description="Append ADR 0010 gate receipt",
        epilog="Plan must name metrics + gate id before generate; verify fails if implementation.py is newer than last PASS.",
    )
    parser.add_argument(
        "--describe",
        action="store_true",
        help="Print R27 binder summary (docs/nlc/GATE-RECORD-BINDER.md)",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--artifact", help="Repo-relative path")
    parser.add_argument("--gate-id", help="Stable id from the plan row / fitness script")
    parser.add_argument("--outcome", default="PASS")
    parser.add_argument("--command", default="")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.describe:
        doc = Path(__file__).resolve().parents[1] / "docs" / "nlc" / "GATE-RECORD-BINDER.md"
        if doc.is_file():
            text = doc.read_text(encoding="utf-8")
            sys.stdout.write(text)
            if not text.endswith("\n"):
                sys.stdout.write("\n")
        else:
            print("GATE_RECORD:BINDER docs/nlc/GATE-RECORD-BINDER.md")
        return 0
    if not args.artifact or not args.gate_id:
        print("gate-record needs --artifact and --gate-id (or --describe).", file=sys.stderr)
        return 2
    if args.outcome != "PASS":
        print("gate-record: only PASS receipts are stored for verify", file=sys.stderr)
        return 1
    append_record(
        root,
        artifact=args.artifact,
        gate_id=args.gate_id,
        outcome=args.outcome,
        command=args.command or None,
    )
    print(f"gate-record: MET artifact={args.artifact}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
