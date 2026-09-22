#!/usr/bin/env python3
"""UC1: validate .nlc/interview-packet.json against integrity schema (minimal)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "integrity" / "schemas" / "interview-packet.schema.json"


def validate(data: dict) -> list[str]:
    bad: list[str] = []
    if data.get("schema") != 1:
        bad.append("schema must be 1")
    for key in ("outcome", "goals", "requirements", "knowledge_domains", "bind_ready"):
        if key not in data:
            bad.append(f"missing {key}")
    if not isinstance(data.get("goals"), list) or not data.get("goals"):
        bad.append("goals must be non-empty array")
    if not isinstance(data.get("requirements"), list) or not data.get("requirements"):
        bad.append("requirements must be non-empty array")
    if not isinstance(data.get("knowledge_domains"), list) or not data.get("knowledge_domains"):
        bad.append("knowledge_domains must be non-empty array")
    if data.get("bind_ready") is not True:
        bad.append("bind_ready must be true")
    if not str(data.get("outcome", "")).strip():
        bad.append("outcome required")
    return bad


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate-interview-packet.py <path-to-interview-packet.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    if not path.is_file():
        print(f"INTERVIEW_PACKET:NOT_MET missing {path}", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"INTERVIEW_PACKET:NOT_MET invalid json: {exc}", file=sys.stderr)
        return 1
    if not SCHEMA.is_file():
        print("INTERVIEW_PACKET:NOT_MET missing schema file", file=sys.stderr)
        return 1
    bad = validate(data)
    if bad:
        print("INTERVIEW_PACKET:NOT_MET " + "; ".join(bad))
        return 1
    print("INTERVIEW_PACKET:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
