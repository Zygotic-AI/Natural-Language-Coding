"""ADR 0029: snapshot ACTIVE set at bind time for reproducibility."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from nlc_adr_active import bind_snapshot_payload  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Write ADR bind snapshot from ACTIVE.md")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(".nlc/adr-bind-snapshot.json"),
        help="Output path under --root (default: .nlc/adr-bind-snapshot.json)",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    active_path = ROOT / "adrs" / "ACTIVE.md"
    if not active_path.is_file():
        print("BIND_SNAPSHOT:NOT_MET missing adrs/ACTIVE.md", file=sys.stderr)
        return 1
    payload = bind_snapshot_payload(active_path.read_text(encoding="utf-8"))
    out = args.out if args.out.is_absolute() else root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"BIND_SNAPSHOT:MET path={out} sha256={payload['active_sha256'][:12]}… "
        f"count={len(payload['adrs'])}"
    )
    return 0


