#!/usr/bin/env python3
"""Validate .nlc/pack-ingest-candidates.json (requirement packs v0.2)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.pack_ingest_candidates import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
