#!/usr/bin/env python3
"""Converge integrity/hub-content-tree-hash.txt (ADR 0050)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.evidence_ref.sync_content_tree_hash import main

if __name__ == "__main__":
    sys.exit(main())
