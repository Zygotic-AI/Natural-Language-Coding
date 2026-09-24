"""SSOT: pending ADR status scan (dashboard, verify, CI)."""

from __future__ import annotations

import re
from pathlib import Path

BOUNDARY = "bba-emit"

PENDING_ADR_STATUS = re.compile(
    r"^\s*-\s*Status:\s*(Proposed|needs_review)\s*$",
    re.I | re.M,
)


def list_pending_adrs(adrs_dir: Path) -> list[str]:
    if not adrs_dir.is_dir():
        return []
    pending: list[str] = []
    for path in sorted(adrs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if PENDING_ADR_STATUS.search(text):
            pending.append(path.name)
    return pending
