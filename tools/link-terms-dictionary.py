#!/usr/bin/env python3
"""Link dictionary terms in markdown to docs/TERMS.md#anchor (one pass, longest match first)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.link_terms_dictionary import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
