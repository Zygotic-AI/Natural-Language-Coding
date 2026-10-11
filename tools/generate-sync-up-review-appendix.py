#!/usr/bin/env python3
"""Thin entrypoint: sync-up review appendix (O4)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.evidence_ref.sync_up_review_appendix_gen import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
