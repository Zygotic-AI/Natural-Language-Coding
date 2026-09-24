#!/usr/bin/env python3
"""Binder: Build a compiled system — UC dependency tools wired in hub CI."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]

TOOLS = (
    "nlc_uc_blockers.py",
    "nlc_language_scan.py",
    "nlc-brownfield-migrate.py",
    "nlc-pack-ingest.py",
    "nlc_rule_runner.py",
    "nlc_call_tree.py",
    "nlc_primitive_propose.py",
    "nlc_generate_provenance.py",
)

LANDMINES = (
    "assert-interview-packet-fails.py",
    "assert-adopter-verify-fast-green-passes.py",
)

FITNESS_HOOKS = (
    "fitness-brownfield-rule-trace.py",
    "fitness-nlc-adopt-existing-hints.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = read_tool("tools/ci_fitness.py")
    comp = read_tool("tools/nlc_compliance.py")
    if "interview_packet_blockers" not in comp:
        violations.append("nlc_compliance must call interview_packet_blockers")
    if "ensure_before_generate_stamp" not in read_tool("tools/nlc_rule_emit.py"):
        violations.append("nlc_rule_emit must enforce before-generate stamp")
    for name in TOOLS:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
    for name in LANDMINES:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
        elif name.replace(".py", "") not in ci and name.split("-")[0] not in ci:
            violations.append(f"ci_fitness must run {name}")
    planit = (ROOT / ".agents" / "skills" / "planit" / "SKILL.md").read_text(
        encoding="utf-8", errors="replace"
    )
    if "jidoka" not in planit or "root-cause" not in planit.lower():
        violations.append("planit SKILL must prescribe UC10 jidoka/RCA on failure")
    interview = (ROOT / ".agents" / "skills" / "interview" / "SKILL.md").read_text(
        encoding="utf-8", errors="replace"
    )
    if "interview-packet" not in interview:
        violations.append("interview SKILL must mention interview-packet.json handoff")
    delta_paths = [
        ROOT / "tools" / "nlc-delta-regen.py",
        ROOT / "tools" / "nouns" / "delta_regen" / "delta_regen.py",
    ]
    delta = "\n".join(
        p.read_text(encoding="utf-8", errors="replace") for p in delta_paths if p.is_file()
    )
    if "goals_for_rule_change" not in delta:
        violations.append("nlc-delta-regen must use goals_for_rule_change (UC9)")
    packs = read_tool("tools/nlc-pack-install.py")
    if "requirements-sync-pending" not in packs:
        violations.append("pack install must flag UC9 regen pending")
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

