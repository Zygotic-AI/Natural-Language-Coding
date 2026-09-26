"""Landmine ADR 0044: main purity logic MET when head equals tag commit."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from nouns.release_main_purity import check_main_purity  # noqa: E402

BOUNDARY = "bba-emit"


def main() -> int:
    ok, probs = check_main_purity(head="abc123", tag="v1.0.0", tag_at="abc123")
    if not ok or probs:
        print("ASSERT:FAIL purity should MET when head equals tag commit")
        return 1
    ok2, probs2 = check_main_purity(head="def456", tag="v1.0.0", tag_at="abc123")
    if ok2 or not probs2:
        print("ASSERT:FAIL purity should NOT_MET when head differs")
        return 1
    print("ASSERT:PASS release main purity logic (ADR 0044)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
