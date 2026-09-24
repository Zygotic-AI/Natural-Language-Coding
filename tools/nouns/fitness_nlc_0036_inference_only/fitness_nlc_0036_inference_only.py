#!/usr/bin/env python3
"""ADR 0036 gate: human surface asks for goal + policy only (default-closed scan)."""

from __future__ import annotations



import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

SURFACES = [
    "docs/nlc/compiler/INTENT-SURFACE.md",
    "docs/nlc/compiler/MANIFESTO.md",
    ".agents/skills/interview/SKILL.md",
]

VIOLATIONS = [
    (
        re.compile(
            r"human[s]?\s+(?:must|should|need to|are asked to)\s+"
            r"(?:name|author|supply|provide|write|fill in)\s+"
            r"(?:an?\s+)?(?:ADR|rule|plan|anchor|manifest|tag)",
            re.I,
        ),
        "human asked to author a derived artifact",
    ),
    (
        re.compile(
            r"ask the (?:human|user) to (?:name|choose|select|provide) "
            r"(?:the )?(?:ADR|rule id|thought anchor|manifest)",
            re.I,
        ),
        "human asked to select ADR/rule/anchor/manifest",
    ),
    (
        re.compile(r"humans? (?:focus on|contribute|provide) (?:three|3) things", re.I),
        "human surface lists three inputs; ADR 0036 allows goal+policy only",
    ),
    (
        re.compile(r"structured fields? from the human", re.I),
        "human surface collects structured fields",
    ),
]


def main() -> int:
    _ = sys.argv[1:]
    failures: list[str] = []
    for rel in SURFACES:
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"MISSING surface: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for rx, label in VIOLATIONS:
            if rx.search(text):
                failures.append(f"{rel}: {label}")
    if failures:
        print("FAIL fitness-nlc-0036-inference-only")
        for item in failures:
            print(" -", item)
        return 1
    print("PASS fitness-nlc-0036-inference-only")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

