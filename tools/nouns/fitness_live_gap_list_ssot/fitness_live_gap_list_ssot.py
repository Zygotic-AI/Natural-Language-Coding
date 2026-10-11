#!/usr/bin/env python3
"""Refuse a second live gap list outside FINDINGS.md (O10)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = ROOT / "FINDINGS.md"
STUB_MAX_LINES = 12

SECOND_QUEUE_PATTERNS: tuple[tuple[Path, re.Pattern[str], str], ...] = (
    (
        ROOT / "docs" / "USE-CASES.md",
        re.compile(r"^## Needed \(expansion\)", re.M),
        "USE-CASES must not host a Needed (expansion) gap table",
    ),
    (
        ROOT / "docs" / "JOBS-TO-BE-DONE.md",
        re.compile(r"^\*\*Blocked\*\*", re.M),
        "JOBS-TO-BE-DONE must not define Blocked job gaps (see FINDINGS)",
    ),
    (
        ROOT / "docs" / "JOBS-TO-BE-DONE.md",
        re.compile(r"Blocking gap \(implementation\)", re.M),
        "JOBS-TO-BE-DONE must not host a blocking-gap column",
    ),
)

STUB_PATHS = (
    ROOT / "TODO",
    ROOT / "HOLES.md",
    ROOT / "docs" / "nlc" / "SESSION-FOLLOWTHROUGH.md",
)


def is_gap_stub(path: Path) -> bool:
    if not path.is_file():
        return False
    lines = [ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    if len(lines) > STUB_MAX_LINES:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return "FINDINGS.md" in text and "docs/history" in text


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not FINDINGS.is_file():
        violations.append("missing FINDINGS.md")
    else:
        head = FINDINGS.read_text(encoding="utf-8", errors="replace")[:2000]
        if "Live gap SSOT" not in head:
            violations.append("FINDINGS.md must declare Live gap SSOT in header")

    for path, pattern, msg in SECOND_QUEUE_PATTERNS:
        if path.is_file() and pattern.search(path.read_text(encoding="utf-8", errors="replace")):
            violations.append(msg)

    for stub in STUB_PATHS:
        if not is_gap_stub(stub):
            violations.append(f"{stub.relative_to(ROOT)} must be a short stub pointing at FINDINGS + docs/history")

    archive = ROOT / "docs" / "history" / "findings-planit-waves-archive.md"
    if FINDINGS.is_file():
        findings_body = FINDINGS.read_text(encoding="utf-8", errors="replace")
        if "## Planit Evaluate-NLC wave-1" in findings_body:
            violations.append("FINDINGS must not embed Planit wave queues (use docs/history archive)")

    if not archive.is_file():
        violations.append("missing docs/history/findings-planit-waves-archive.md")

    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
