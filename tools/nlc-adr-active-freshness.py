#!/usr/bin/env python3
"""ADR 0029: fail if ACTIVE changed since bind snapshot (freshness)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_adr_active import bind_snapshot_payload  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Compare bind snapshot to current ACTIVE")
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path(".nlc/adr-bind-snapshot.json"),
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    snap_path = args.snapshot if args.snapshot.is_absolute() else root / args.snapshot
    if not snap_path.is_file():
        print(f"ACTIVE_FRESHNESS:NOT_MET missing snapshot {snap_path}", file=sys.stderr)
        return 1
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    expected = str(snap.get("active_sha256") or "")
    current = bind_snapshot_payload((ROOT / "adrs" / "ACTIVE.md").read_text(encoding="utf-8"))
    got = current["active_sha256"]
    if expected != got:
        print(
            f"ACTIVE_FRESHNESS:NOT_MET snapshot={expected[:12]}… active={got[:12]}… (re-bind required)",
            file=sys.stderr,
        )
        return 1
    print(f"ACTIVE_FRESHNESS:MET sha256={got[:12]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
