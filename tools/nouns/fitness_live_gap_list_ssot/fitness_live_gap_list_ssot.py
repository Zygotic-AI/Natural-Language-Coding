#!/usr/bin/env python3
"""Refuse a second live gap list outside FINDINGS.md (O10)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = ROOT / "FINDINGS.md"
STUB_MAX_LINES = 12

sys.path.insert(0, str(ROOT / "tools"))
from nouns.live_gap_list_ssot.live_gap_list_ssot import scan_repo  # noqa: E402

STUB_PATHS = (
    ROOT / "TODO",
    ROOT / "HOLES.md",
    ROOT / "docs" / "nlc" / "SESSION-FOLLOWTHROUGH.md",
)

REQUIRED_FINDINGS_MARKERS: tuple[str, ...] = (
    "0045 ⊕ 0048 effective-decision view",
    "J1 — semantic apply",
    "J2 — tag blast radius",
    "J7 — full product verify",
    "J8 — rule-tagged narrowing",
    "J20 — bare `engine.runtime`",
    "hub tool interiors still open",
    "full noun/verb rewrite open",
    "R4 — verb belongs on this noun",
    "Python-only language limit",
    "368 of 370",
    "Roadmap §2.4 reconciliations",
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
        head = FINDINGS.read_text(encoding="utf-8", errors="replace")
        if "Live gap SSOT" not in head[:2000]:
            violations.append("FINDINGS.md must declare Live gap SSOT in header")
        if "## Planit Evaluate-NLC wave-1" in head:
            violations.append("FINDINGS must not embed Planit wave queues (use docs/history archive)")
        for marker in REQUIRED_FINDINGS_MARKERS:
            if marker not in head:
                violations.append(f"FINDINGS missing restored gap marker: {marker!r}")

    for stub in STUB_PATHS:
        if not is_gap_stub(stub):
            violations.append(f"{stub.relative_to(ROOT)} must be a short stub pointing at FINDINGS + docs/history")

    archive = ROOT / "docs" / "history" / "findings-planit-waves-archive.md"
    if not archive.is_file():
        violations.append("missing docs/history/findings-planit-waves-archive.md")

    violations.extend(scan_repo(ROOT))

    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
