#!/usr/bin/env python3
"""ADR 0023: hub compiler rule-emit wired to CLI, planit, and CI."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    tool = ROOT / "tools" / "nlc_rule_emit.py"
    if not tool.is_file():
        violations.append("missing tools/nlc_rule_emit.py")
    nlc = read_tool("tools/nlc.py")
    if "rule-emit" not in nlc or "nlc_rule_emit.py" not in nlc:
        violations.append("nlc.py must expose maintainer rule-emit → nlc_rule_emit.py")
    planit = (ROOT / ".agents" / "skills" / "planit" / "SKILL.md").read_text(
        encoding="utf-8", errors="replace"
    )
    if "rule-emit" not in planit:
        violations.append("planit SKILL must prescribe rule-emit after generate")
    proposer = (ROOT / ".agents" / "skills" / "bbp-proposer" / "SKILL.md").read_text(
        encoding="utf-8", errors="replace"
    )
    if "rule-emit" not in proposer and "rule-marker" not in proposer:
        violations.append("bbp-proposer SKILL must prescribe rule emit tools")
    ci = read_tool("tools/ci_fitness.py")
    if "assert-rule-emit-sync" not in ci:
        violations.append("ci_fitness must run assert-rule-emit-sync-passes")
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

