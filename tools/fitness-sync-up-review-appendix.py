#!/usr/bin/env python3
"""O4: committed sync-up appendix matches generator SSOT (302 paths @ 5554b8b)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.evidence_ref.sync_up_review_appendix_gen import verify_committed_appendix  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(verify_committed_appendix())
