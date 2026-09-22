#!/usr/bin/env python3
"""UC4/UC5: materialize and check if/then rule IR (compiler-owned, not prompt memory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nlc_requirements import hub_tool
from nlc_rule_coverage import load_adopted

SNAPSHOT = "rule-ir.snapshot.json"


def materialize_ir(root: Path) -> list[dict]:
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    rows = load_adopted(adopted)
    out: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        out.append(
            {
                "rule_id": row.get("rule_id"),
                "adr_id": row.get("adr_id"),
                "effect": row.get("effect"),
                "obligation": row.get("obligation"),
                "match": row.get("match") or {},
                "precedence_tier": row.get("precedence_tier"),
                "precedence_rank": row.get("precedence_rank"),
            }
        )
    return sorted(out, key=lambda r: str(r.get("rule_id") or ""))


def write_snapshot(root: Path, rows: list[dict]) -> Path:
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    path = nlc / SNAPSHOT
    path.write_text(
        json.dumps({"schema": 1, "rules": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def check_ir(root: Path) -> list[str]:
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    live = materialize_ir(root)
    snap_path = root / ".nlc" / SNAPSHOT
    if not snap_path.is_file():
        return [
            "UC4 rule runner: missing .nlc/rule-ir.snapshot.json "
            "(./nlc maintainer rule-runner --materialize after adopt)"
        ]
    try:
        snap = json.loads(snap_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["UC4 rule runner: invalid rule-ir.snapshot.json"]
    stored = snap.get("rules") or []
    if stored != live:
        return ["UC4 rule runner: adopted.json drifted from rule-ir.snapshot (re-run --materialize)"]
    bad: list[str] = []
    for row in live:
        rid = row.get("rule_id")
        eff = row.get("effect")
        if eff == "must" and not str(row.get("obligation") or "").strip():
            bad.append(f"rule {rid} effect must requires obligation")
        match = row.get("match") or {}
        if not match.get("primitive") and not match.get("tags_all") and not match.get("tags_any"):
            bad.append(f"rule {rid} has empty match")
    if bad:
        return ["UC4 rule runner: " + "; ".join(bad[:4])]
    return []


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
