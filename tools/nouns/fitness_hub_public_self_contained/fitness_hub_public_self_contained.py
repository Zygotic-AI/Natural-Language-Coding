#!/usr/bin/env python3
"""O6: in-force surfaces must not depend on private repos or person names (CG-R4)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.hub_in_force_surfaces.hub_in_force_surfaces import (  # noqa: E402
    PERSON_NAME_EXCLUDED_PREFIXES,
    iter_in_force_files,
)

FORBIDDEN_MARKERS = (
    "BBA-Bindings",
    "richardpickett/BBA-Bindings",
    "github.com/richardpickett/BBA-Bindings",
    "app.notion.com",
    "ai-vault maintainer",
    "ai-vault-only",
)

PERSON_PATTERNS = (
    re.compile(r"Richard\s+Pickett", re.IGNORECASE),
    re.compile(r"richardpickett", re.IGNORECASE),
)

TEXT_SUFFIXES = (".md", ".mdc", ".json", ".txt", ".yaml", ".yml")


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in iter_in_force_files(ROOT, suffixes=TEXT_SUFFIXES):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                violations.append(f"{rel}: forbidden marker {marker!r}")
        rel_posix = rel.as_posix()
        skip_person = any(
            rel_posix == p.rstrip("/") or rel_posix.startswith(p)
            for p in PERSON_NAME_EXCLUDED_PREFIXES
        )
        if not skip_person:
            for pat in PERSON_PATTERNS:
                if pat.search(text):
                    violations.append(f"{rel}: person-name pattern {pat.pattern}")
    take_me = ROOT / ".agents" / "instructions" / "take-me-literally.md"
    if not take_me.is_file():
        violations.append("missing .agents/instructions/take-me-literally.md")
    agents = ROOT / "AGENTS.md"
    if agents.is_file() and "take-me-literally.md" not in agents.read_text(encoding="utf-8"):
        violations.append("AGENTS.md must link take-me-literally.md")

    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
