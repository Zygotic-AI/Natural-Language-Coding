"""KB-0058-hide: main's prefixes still list an ADR the branch copy dropped."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.sensitive_review.sensitive_review import (  # noqa: E402
    is_sensitive,
    sensitive_changes,
)


def main() -> int:
    base = {"adrs/0001-zero-variance-integrity.md": b"old\n"}
    head = {"adrs/0001-zero-variance-integrity.md": b"new\n"}
    main_hits = sensitive_changes(base, head, predicate=is_sensitive)

    def hide_adr(rel: str) -> bool:
        if rel.startswith("adrs/"):
            return False
        return is_sensitive(rel)

    hide_hits = sensitive_changes(base, head, predicate=hide_adr)
    if not main_hits:
        print("ASSERT:FAIL main prefixes did not list the changed ADR")
        return 1
    if hide_hits:
        print("ASSERT:FAIL hiding prefixes still listed the ADR")
        return 1
    print("ASSERT:PASS main copy lists a path the branch copy hid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
