"""Record PLANIT 6.5 gate PASS for an artifact (ADR 0010)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from nlc_requirements import hub_tool

VALID_OUTCOMES = {"PASS", "FAIL", "WAIVED"}


def append_record(
    root: Path,
    *,
    artifact: str,
    gate_id: str,
    outcome: str,
    command: str | None = None,
) -> None:
    if outcome not in VALID_OUTCOMES:
        raise ValueError(f"outcome must be one of {VALID_OUTCOMES}")
    rel = artifact.replace("\\", "/").lstrip("./")
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    path = nlc / "gate-records.json"
    records: list[dict] = []
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            records = list(data.get("records") or [])
        except json.JSONDecodeError:
            records = []
    records.append(
        {
            "artifact": rel,
            "gate_id": gate_id,
            "outcome": outcome,
            "command": command or "",
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )
    path.write_text(
        json.dumps({"schema": 1, "records": records}, indent=2) + "\n",
        encoding="utf-8",
    )


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
