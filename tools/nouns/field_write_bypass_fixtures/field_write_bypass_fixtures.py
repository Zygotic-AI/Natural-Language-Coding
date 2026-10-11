"""O9a: exact invoice-bypass fixture folder names (no wildcard)."""

from __future__ import annotations

O9A_BYPASS_FIXTURE_DIRS: frozenset[str] = frozenset(
    {
        "invoice-bypass-object-setattr-violation",
        "invoice-bypass-setattr-violation",
        "invoice-bypass-dict-violation",
        "invoice-bypass-multiline-violation",
    }
)
