#!/usr/bin/env python3
"""A11 permanence: CHARTER.md first H1 must open as NLC roof (not BBP-only)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARTER = ROOT / "CHARTER.md"


def main() -> int:
    _ = sys.argv[1:]
    text = CHARTER.read_text(encoding="utf-8", errors="replace")
    # First markdown H1 only
    first_h1 = ""
    for line in text.splitlines():
        if line.startswith("# "):
            first_h1 = line
            break
    if not first_h1:
        print("VIOLATION CHARTER.md has no H1")
        print("RESULT:NOT_MET")
        return 1
    lowered = first_h1.lower()
    if "natural language coding" not in lowered and "nlc" not in lowered:
        print(f"VIOLATION CHARTER first H1 must name NLC roof; got: {first_h1!r}")
        print("RESULT:NOT_MET")
        return 1
    if lowered.startswith("# [boundary-based programming]") or lowered.startswith(
        "# boundary-based programming"
    ):
        print(f"VIOLATION CHARTER first H1 must not be BBP-only door; got: {first_h1!r}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
