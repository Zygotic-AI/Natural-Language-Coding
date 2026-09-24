#!/usr/bin/env python3
"""ADR 0025: validate RCA packet JSON (schema + no-blame climb rules)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "integrity" / "schemas" / "rca-packet.schema.json"

BLAME_ONLY = [
    re.compile(r"^\s*(the\s+)?agent\s+(caused|failed|is\s+at\s+fault)", re.I),
    re.compile(r"^\s*human\s+error\s*$", re.I),
    re.compile(r"^\s*operator\s+fault\s*$", re.I),
    re.compile(r"^\s*developer\s+mistake\s*$", re.I),
]


def _schema_check(data: dict) -> list[str]:
    bad: list[str] = []
    if data.get("schema") != 1:
        bad.append("schema must be 1")
    for key in ("defect_summary", "unsuitable_process", "climb_steps", "repo_touch"):
        if key not in data:
            bad.append(f"missing {key}")
    climb = data.get("climb_steps")
    if not isinstance(climb, list) or not climb:
        bad.append("climb_steps must be non-empty array")
    touch = data.get("repo_touch")
    if not isinstance(touch, dict):
        bad.append("repo_touch must be object")
        return bad
    belief = str(touch.get("belief", "")).strip()
    adr_ids = touch.get("adr_ids") or []
    rule_ids = touch.get("rule_ids") or []
    gate_ids = touch.get("gate_ids") or []
    if not belief and not adr_ids and not rule_ids and not gate_ids:
        bad.append("repo_touch must cite belief and/or adr_ids/rule_ids/gate_ids")
    return bad


def _policy_check(data: dict) -> list[str]:
    bad: list[str] = []
    process = str(data.get("unsuitable_process", "")).strip()
    if not process:
        bad.append("unsuitable_process required")
        return bad
    for rx in BLAME_ONLY:
        if rx.search(process):
            bad.append("unsuitable_process must name a process, not agent/human blame only")
            break
    if re.search(r"\b(agent|human|operator|developer)\s+(caused|at fault)\b", process, re.I):
        if "process" not in process.lower() and "procedure" not in process.lower():
            bad.append("root cause must climb to process language (ADR 0025)")
    climb = data.get("climb_steps") or []
    if len(climb) < 1:
        bad.append("at least one climb step required")
    return bad


def validate_data(data: dict) -> list[str]:
    return _schema_check(data) + _policy_check(data)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate-rca-packet.py <path-to-rca-packet.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    if not path.is_file():
        print(f"RCA_PACKET:NOT_MET missing {path}", file=sys.stderr)
        return 1
    if not SCHEMA.is_file():
        print("RCA_PACKET:NOT_MET missing integrity/schemas/rca-packet.schema.json", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"RCA_PACKET:NOT_MET invalid JSON: {exc}", file=sys.stderr)
        return 1
    bad = validate_data(data)
    if bad:
        print("RCA_PACKET:NOT_MET", file=sys.stderr)
        for item in bad:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("RCA_PACKET:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
