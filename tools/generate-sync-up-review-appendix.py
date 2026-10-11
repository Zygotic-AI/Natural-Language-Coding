#!/usr/bin/env python3
"""Thin entrypoint: sync-up review appendix (O4)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.sync_up_review_appendix.sync_up_review_appendix import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
