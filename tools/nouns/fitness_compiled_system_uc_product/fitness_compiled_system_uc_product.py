#!/usr/bin/env python3
"""Product slice: UC tools wired and green specimen commands MET."""

from __future__ import annotations



import subprocess
import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]

TOOLS = (
    "nlc_rule_runner.py",
    "nlc_call_tree.py",
    "nlc_primitive_propose.py",
    "nlc_generate_provenance.py",
    "nlc_todo_ssot.py",
)

NLC_MARKERS = (
    "rule-runner",
    "call-tree",
    "primitive-propose",
)

SPECIMEN = ROOT / "examples" / "adopter-verify-fast-green"
STATUS = ROOT / "integrity" / "uc-product-status.json"


def _run(argv: list[str]) -> bool:
    proc = subprocess.run(argv, cwd=str(ROOT), capture_output=True, text=True)
    return proc.returncode == 0


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not STATUS.is_file():
        violations.append("missing integrity/uc-product-status.json")
    for name in TOOLS:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
    nlc = read_tool("tools/nlc.py")
    for marker in NLC_MARKERS:
        if marker not in nlc:
            violations.append(f"nlc.py maintainer must expose {marker}")
    skill = ROOT / ".agents" / "skills" / "requirement-pack-ingest" / "SKILL.md"
    if not skill.is_file():
        violations.append("missing requirement-pack-ingest skill")
    comp = read_tool("tools/nlc_compliance.py")
    for fn in (
        "proposed_adr_blockers",
        "interview_requirements_sync_blockers",
        "rule_runner_blockers",
        "goal_bindings_narrow_blockers",
        "engine_runtime_tag_strict_blockers",
        "call_tree_blockers",
        "non_python_adapter_blockers",
        "upstream_hand_patch_blockers",
    ):
        if fn not in comp:
            violations.append(f"nlc_compliance verify must wire {fn}")
    ssot = read_tool("tools/fitness-todo-use-cases-ssot.py")
    if "uc-product-status" not in ssot and "nlc_todo_ssot" not in ssot:
        violations.append("SSOT fitness must use integrity/uc-product-status.json (not hollow)")
    if SPECIMEN.is_dir():
        if not _run(
            [
                sys.executable,
                str(ROOT / "tools" / "nlc_rule_runner.py"),
                "--root",
                str(SPECIMEN),
                "--check",
            ]
        ):
            violations.append("adopter-verify-fast-green rule-runner --check must MET")
        pkt = SPECIMEN / ".nlc" / "interview-packet.json"
        if pkt.is_file() and not _run(
            [sys.executable, str(ROOT / "tools" / "validate-interview-packet.py"), str(pkt)]
        ):
            violations.append("adopter interview-packet must validate")
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

