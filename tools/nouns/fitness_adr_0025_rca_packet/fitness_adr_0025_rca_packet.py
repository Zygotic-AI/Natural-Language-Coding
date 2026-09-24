#!/usr/bin/env python3
"""ADR 0025 expansion: RCA packet schema + validator wired."""

from __future__ import annotations



import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "integrity" / "schemas" / "rca-packet.schema.json"
VALIDATOR = ROOT / "tools" / "validate-rca-packet.py"
RULES = ROOT / "rules" / "nlc-0025.json"
OK = ROOT / "examples" / "rca-packet-ok" / "rca-packet.json"
BAD = ROOT / "examples" / "rca-packet-blame-agent" / "rca-packet.json"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path, label in (
        (SCHEMA, "rca-packet.schema.json"),
        (VALIDATOR, "validate-rca-packet.py"),
        (RULES, "nlc-0025.json"),
        (OK, "rca-packet-ok specimen"),
    ):
        if not path.is_file():
            violations.append(f"missing {label}")
    if RULES.is_file():
        text = RULES.read_text(encoding="utf-8")
        if "expansion: rca-packet-schema" in text:
            violations.append("nlc-0025.json still lists expansion gate")
        if "validate-rca-packet.py" not in text:
            violations.append("nlc-0025.json must cite validate-rca-packet.py")
    if OK.is_file() and VALIDATOR.is_file():
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), str(OK)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            violations.append("ok specimen must MET validate-rca-packet")
    if BAD.is_file() and VALIDATOR.is_file():
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), str(BAD)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            violations.append("blame-agent specimen must NOT_MET")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

