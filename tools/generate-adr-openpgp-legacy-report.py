#!/usr/bin/env python3
"""Regenerate integrity/adr-openpgp-legacy-report.txt (ADR 0052 P2)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_REL = "integrity/adr-openpgp-legacy-report.txt"
_STATUS = re.compile(r"^-\s*Status:\s*(\S+)", re.M)


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.adr_approval.adr_approval import active_numbers

    lines: list[str] = []
    for number in active_numbers((ROOT / "adrs" / "ACTIVE.md").read_text(encoding="utf-8")):
        n = int(number)
        if n > 51:
            continue
        matches = sorted((ROOT / "adrs").glob(f"{number}-*.md"))
        if len(matches) != 1:
            continue
        text = matches[0].read_text(encoding="utf-8")
        status_match = _STATUS.search(text)
        if not status_match or status_match.group(1) != "Accepted":
            continue
        lines.append(f"{number} unsigned (legacy hash receipt)")
    body = "\n".join(lines) + ("\n" if lines else "")
    (ROOT / REPORT_REL).write_text(body, encoding="utf-8")
    print(f"wrote {REPORT_REL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
