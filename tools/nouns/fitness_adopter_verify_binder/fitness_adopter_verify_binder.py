#!/usr/bin/env python3
"""ADR 0021/0023: adopter verify-fast green specimen + landmine in CI."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    fixture = ROOT / "examples" / "adopter-verify-fast-green"
    if not fixture.is_dir():
        violations.append("missing examples/adopter-verify-fast-green")
    for rel in (
        "examples/adopter-verify-fast-green/.nlc/interview-packet.json",
        "examples/adopter-verify-fast-green/.nlc/before-generate-stamp.json",
        "examples/adopter-verify-fast-green/.nlc/gate-records.json",
        "examples/adopter-verify-fast-green/.nlc/produce-package.json",
        "examples/adopter-verify-fast-green/.nlc/change-adversarial.json",
        "examples/adopter-verify-fast-green/.nlc/verified.json",
        "examples/adopter-verify-fast-green/rules/adopted.json",
    ):
        if not (ROOT / rel).is_file():
            violations.append(f"missing {rel}")
    ci = read_tool("tools/ci_fitness.py")
    if "assert-adopter-verify-fast-green" not in ci:
        violations.append("ci_fitness must run assert-adopter-verify-fast-green-passes")
    doc = ROOT / "docs" / "nlc" / "RULE-TRACE.md"
    if doc.is_file() and "adopter-verify-fast-green" not in doc.read_text(encoding="utf-8", errors="replace"):
        violations.append("RULE-TRACE.md should cite adopter-verify-fast-green specimen")
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

