"""Landmine ADR 0010: rejected batch-only policy must stay documented as fail-closed."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ADR = ROOT / "adrs" / "0010-gate-after-every-generate.md"


from markdown_plain import strip_links


def main() -> int:
    text = strip_links(ADR.read_text(encoding="utf-8"))
    if "Batch generate, prove once at the end" not in text:
        print("ASSERT:FAIL ADR 0010 must reject batch generate")
        return 1
    if "Soft-fail / warn and continue" not in text:
        print("ASSERT:FAIL ADR 0010 must reject soft-fail continue")
        return 1
    print("ASSERT:PASS ADR 0010 rejects batch-only and soft-fail")
    return 0


