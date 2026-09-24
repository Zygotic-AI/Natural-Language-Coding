#!/usr/bin/env python3
"""ADR 0018: human-facing hub tools use interview-shaped gaps (not NOT_MET-first)."""

from __future__ import annotations



import re
import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]

EMIT_GAP_MODULES = (
    "tools/nlc.py",
    "tools/nlc_cli_help.py",
    "tools/nlc-pack-export.py",
    "tools/nlc-pack-install.py",
)

INTERVIEW_SHAPE_MODULES = (
    "tools/nlc_requirements.py",
    "tools/nlc-install-verify.py",
    "tools/nlc-update.py",
    "tools/nlc_distribution.py",
)

INTERVIEW_SHAPE_SCRIPTS = (
    "scripts/install.sh",
    "scripts/install.ps1",
)

NOT_MET_FIRST_RE = re.compile(
    r'print\(\s*["\']([A-Z][A-Z0-9_]*):NOT_MET',
)


def violations_for(path: Path, rel: str) -> list[str]:
    text = read_tool(rel)
    out: list[str] = []
    if rel in EMIT_GAP_MODULES and "emit_gap" not in text:
        out.append(f"{rel} must use nlc_human_gap.emit_gap (ADR 0018 reference)")
    if rel in INTERVIEW_SHAPE_MODULES and "What's wrong:" not in text:
        out.append(f"{rel} must list gaps with 'What's wrong:' before machine tokens")
    for m in NOT_MET_FIRST_RE.finditer(text):
        start = m.start()
        before = text[max(0, start - 400) : start]
        if "file=sys.stderr" not in before and "stderr" not in before:
            continue
        if "What's wrong:" not in before and "emit_gap" not in before:
            snippet = text[start : start + 60].splitlines()[0]
            out.append(f"{rel} prints NOT_MET without prior interview text: {snippet[:50]}…")
    return out


def main() -> int:
    # Hub-only (ADR 0018). release-audit passes an adopter tree; scan the hub repo root.
    _ = sys.argv[1:]  # ignored — same pattern as fitness-menu-harness-sync / fitness-nlc-naming
    rel_set = set(EMIT_GAP_MODULES) | set(INTERVIEW_SHAPE_MODULES)
    violations: list[str] = []
    for rel in sorted(rel_set):
        path = ROOT / rel
        if not path.is_file():
            violations.append(f"missing {rel}")
            continue
        violations.extend(violations_for(path, rel))
    for rel in INTERVIEW_SHAPE_SCRIPTS:
        path = ROOT / rel
        if not path.is_file():
            violations.append(f"missing {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "What's wrong:" not in text:
            violations.append(f"{rel} must list gaps with 'What's wrong:' before machine tokens")
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

