#!/usr/bin/env python3
"""Landmine: a different Planit skill does not match this repository's registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.planit_identity import identity_errors, load_registry


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = load_registry(root)
    errors = identity_errors(registry, "other/planit/SKILL.md", b"other planit skill\n")
    if len(errors) < 2:
        print("ASSERT:FAIL other Planit must fail path and hash")
        return 1
    handoff = {
        "planit_skill_path": "other/planit/SKILL.md",
        "planit_skill_sha256": "0" * 64,
    }
    from nouns.planit_identity import handoff_errors

    if not handoff_errors(handoff, registry):
        print("ASSERT:FAIL handoff must reject the other Planit")
        return 1
    print("ASSERT:PASS other Planit is refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
