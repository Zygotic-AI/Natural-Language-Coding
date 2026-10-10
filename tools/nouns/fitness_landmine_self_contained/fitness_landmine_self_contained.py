#!/usr/bin/env python3
"""Release landmines must not pin resolvable hub commit ids (ADR 0050)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.evidence_ref.evidence_ref import commit_pins_in_text  # noqa: E402

LANDMINES = (
    ROOT / "tools" / "nouns" / "assert_release_tag_gate_fails" / "assert_release_tag_gate_fails.py",
    ROOT
    / "tools"
    / "nouns"
    / "assert_shipped_tag_audit_fails"
    / "assert_shipped_tag_audit_fails.py",
    ROOT / "tools" / "nouns" / "assert_release_state_passes" / "assert_release_state_passes.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in LANDMINES:
        if not path.is_file():
            violations.append(f"missing landmine {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "BAD_COMMIT" in text:
            violations.append(f"{path.name} still defines BAD_COMMIT")
        pins = commit_pins_in_text(ROOT, text)
        if pins:
            violations.append(f"{path.relative_to(ROOT)} pins hub commits: {', '.join(pins)}")
        if "synthetic_release" not in text and "unprepared_release_commit" not in text:
            if "assert_release_state_passes" not in path.name:
                violations.append(f"{path.relative_to(ROOT)} must build synthetic repo")

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
