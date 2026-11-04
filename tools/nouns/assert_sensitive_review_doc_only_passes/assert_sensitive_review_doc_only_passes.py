"""KB-0058-doc: a docs/rca-only change is not on the sensitive list."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.sensitive_review.sensitive_review import sensitive_changes  # noqa: E402


def main() -> int:
    base = {"docs/rca/example.md": b"old\n"}
    head = {"docs/rca/example.md": b"new\n"}
    hits = sensitive_changes(base, head)
    if hits:
        print(f"ASSERT:FAIL doc-only change listed as sensitive: {hits!r}")
        return 1
    print("ASSERT:PASS doc-only change is not on the sensitive list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
