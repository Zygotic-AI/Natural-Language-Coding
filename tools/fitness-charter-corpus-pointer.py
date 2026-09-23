#!/usr/bin/env python3
"""E1: CHARTER.md or CHARTER-CORPUS.md must point at integrity/rule-corpus.json."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLE = "integrity/rule-corpus.json"


def main() -> int:
    _ = sys.argv[1:]
    charter = ROOT / "CHARTER.md"
    pointer = ROOT / "docs" / "nlc" / "CHARTER-CORPUS.md"
    texts = []
    for path in (charter, pointer):
        if path.is_file():
            texts.append(path.read_text(encoding="utf-8", errors="replace"))
    if not any(NEEDLE in t for t in texts):
        print("VIOLATION neither CHARTER.md nor CHARTER-CORPUS.md cites integrity/rule-corpus.json")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
