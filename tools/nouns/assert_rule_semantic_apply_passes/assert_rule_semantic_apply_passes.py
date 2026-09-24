"""Landmine UC5 v2: semantic apply MET when obligation receipt present."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "rule-semantic-apply-must-ok"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.rule_receipt.rule_receipt import check_semantic_apply

    errs = check_semantic_apply(FIXTURE.resolve())
    if errs:
        print("\n".join(errs))
        print("ASSERT:FAIL semantic apply should MET on rule-semantic-apply-must-ok")
        return 1
    print("ASSERT:PASS semantic apply MET (UC5 v2)")
    return 0
