#!/usr/bin/env python3
"""Code gap-list exclusions must match integrity/GAP-LIST-SSOT-EXCLUSIONS.md (O10)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / "integrity" / "GAP-LIST-SSOT-EXCLUSIONS.md"

sys.path.insert(0, str(ROOT / "tools"))
from nouns.live_gap_list_ssot.gap_list_exclusions import documented_exclusion_rows  # noqa: E402


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not DOC.is_file():
        violations.append("missing GAP-LIST-SSOT-EXCLUSIONS.md")
        print("RESULT:NOT_MET")
        return 1

    doc_text = DOC.read_text(encoding="utf-8", errors="replace")
    for kind, loc, reason in documented_exclusion_rows():
        if kind in ("prefix", "exact", "skill_prefix"):
            if loc not in doc_text:
                violations.append(f"GAP-LIST-SSOT-EXCLUSIONS.md missing path {loc!r}")
            if reason not in doc_text:
                violations.append(f"GAP-LIST-SSOT-EXCLUSIONS.md missing reason for {loc!r}")
        elif kind == "line":
            file_part = loc.split(" :: ", 1)[0]
            token = f"line:{file_part}"
            if token not in doc_text and file_part not in doc_text:
                violations.append(f"GAP-LIST-SSOT-EXCLUSIONS.md missing line exemption {file_part!r}")
            if reason not in doc_text:
                violations.append(f"GAP-LIST-SSOT-EXCLUSIONS.md missing line reason for {file_part!r}")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
