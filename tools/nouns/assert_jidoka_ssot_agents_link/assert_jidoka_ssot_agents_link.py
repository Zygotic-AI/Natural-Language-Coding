"""Landmine: jidoka SSOT output instruction wired in AGENTS.md + release skill (RCA 26-09-25)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

BOUNDARY = "bba-emit"


def main() -> int:
    _ = sys.argv[1:]
    agents = ROOT / "AGENTS.md"
    instruction = ROOT / ".agents" / "instructions" / "jidoka-ssot-output.md"
    release_skill = ROOT / ".agents" / "skills" / "release" / "SKILL.md"
    rca = ROOT / "docs" / "rca" / "2026-09-25-agent-counseled-ignore-tooling-defect.md"

    for path, label in (
        (agents, "AGENTS.md"),
        (instruction, "jidoka-ssot-output.md"),
        (release_skill, "release SKILL.md"),
        (rca, "RCA record"),
    ):
        if not path.is_file():
            print(f"ASSERT:FAIL missing {label}")
            return 1

    agents_text = agents.read_text(encoding="utf-8")
    if "jidoka-ssot-output.md" not in agents_text:
        print("ASSERT:FAIL AGENTS.md must link jidoka-ssot-output.md")
        return 1
    if "ignore or reinterpret" not in agents_text.lower() and "do **not** tell them to ignore" not in agents_text:
        print("ASSERT:FAIL AGENTS.md must forbid ignore/reinterpret counseling")
        return 1

    inst_text = instruction.read_text(encoding="utf-8")
    if "## Gate (default-closed)" not in inst_text or "No ignore counseling" not in inst_text:
        print("ASSERT:FAIL jidoka-ssot-output.md missing default-closed gate")
        return 1

    skill_text = release_skill.read_text(encoding="utf-8")
    if "jidoka-ssot-output.md" not in skill_text:
        print("ASSERT:FAIL release skill must cite jidoka-ssot-output.md")
        return 1

    print("ASSERT:PASS jidoka SSOT output portable link (RCA 26-09-25)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
