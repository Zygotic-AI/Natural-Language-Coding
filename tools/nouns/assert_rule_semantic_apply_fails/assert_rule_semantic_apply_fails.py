"""Landmine UC5 v2: semantic apply NOT_MET when obligation receipt missing."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "rule-semantic-apply-must-violation"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.rule_receipt.rule_receipt import check_semantic_apply

    errs = check_semantic_apply(FIXTURE.resolve())
    if not errs:
        print("ASSERT:FAIL semantic apply should NOT_MET on missing obligation receipt")
        return 1
    print("ASSERT:PASS semantic apply refuses marker-only must rule (UC5 v2)")
    return 0
