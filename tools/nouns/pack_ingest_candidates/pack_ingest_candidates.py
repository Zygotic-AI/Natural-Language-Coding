"""Validate .nlc/pack-ingest-candidates.json (requirement packs v0.2)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOUNDARY = "bba-emit"


def validate(data: dict) -> list[str]:
    bad: list[str] = []
    if data.get("schema") != 1:
        bad.append("schema must be 1")
    if not str(data.get("source", "")).strip():
        bad.append("source required")
    adrs = data.get("candidate_adrs")
    if not isinstance(adrs, list) or not adrs:
        bad.append("candidate_adrs must be non-empty array")
    else:
        for i, row in enumerate(adrs):
            if not isinstance(row, dict):
                bad.append(f"candidate_adrs[{i}] must be object")
                continue
            if not str(row.get("title", "")).strip():
                bad.append(f"candidate_adrs[{i}] missing title")
            if not isinstance(row.get("requirements"), list) or not row.get("requirements"):
                bad.append(f"candidate_adrs[{i}] requirements required")
    if not str(data.get("ratify", "")).strip():
        bad.append("ratify instruction required")
    return bad


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 1:
        print("usage: validate-pack-ingest-candidates.py <path>", file=sys.stderr)
        return 2
    path = Path(args[0]).resolve()
    if not path.is_file():
        print("PACK_INGEST_CANDIDATES:NOT_MET missing file", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("PACK_INGEST_CANDIDATES:NOT_MET invalid json", file=sys.stderr)
        return 1
    bad = validate(data)
    if bad:
        print("PACK_INGEST_CANDIDATES:NOT_MET " + "; ".join(bad))
        return 1
    print("PACK_INGEST_CANDIDATES:MET")
    return 0
