#!/usr/bin/env python3
"""ADR 0023: rule trace CLI, coverage, gate, and skill prescriptions in CI."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]

LANDMINES = (
    "assert-rule-coverage-fails.py",
    "assert-rule-coverage-passes.py",
    "assert-hub-rule-coverage-passes.py",
    "assert-verify-rule-coverage-blockers-fails.py",
    "assert-verify-rule-coverage-blockers-passes.py",
    "assert-verify-rule-marker-gate-fails.py",
    "assert-rule-marker-emit.py",
    "assert-goal-scaffold-emits-markers.py",
    "assert-rule-emit-sync-passes.py",
)

FITNESS = (
    "fitness-planit-generate-markers.py",
    "fitness-planit-noun-shape.py",
    "fitness-verify-skill-binders.py",
    "fitness-verify-rule-coverage-wired.py",
    "fitness-nlc-rule-emit-wired.py",
    "fitness-brownfield-rule-trace.py",
    "fitness-nlc-adopt-existing-hints.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = read_tool("tools/ci_fitness.py")
    for name in LANDMINES + FITNESS:
        path = ROOT / "tools" / name
        if not path.is_file():
            violations.append(f"missing tools/{name}")
            continue
        stem = name.removesuffix("-passes.py").removesuffix("-fails.py").removesuffix(".py")
        if stem not in ci and name not in ci:
            violations.append(f"ci_fitness must run {name}")
    for rel in ("tools/nlc_rule_coverage.py", "tools/nlc_rule_marker.py", "tools/nlc_goal_scaffold.py"):
        if not (ROOT / rel).is_file():
            violations.append(f"missing {rel}")
    planit = (ROOT / ".agents/skills/planit/SKILL.md").read_text(encoding="utf-8", errors="replace")
    if "rule-marker" not in planit or "nlc:rule=" not in planit:
        violations.append("planit SKILL must prescribe rule markers")
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

