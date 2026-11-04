"""KB-0058-self: editing the list-builder lists the list-builder."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.sensitive_review.sensitive_review import (  # noqa: E402
    LISTER_REL,
    sensitive_changes,
)


def main() -> int:
    base = {LISTER_REL: b"old\n"}
    head = {LISTER_REL: b"new\n"}
    hits = sensitive_changes(base, head)
    if not any(rel == LISTER_REL for rel, _digest in hits):
        print("ASSERT:FAIL list-builder edit was not listed")
        return 1
    print("ASSERT:PASS list-builder lists itself")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
