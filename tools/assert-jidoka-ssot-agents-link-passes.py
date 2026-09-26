#!/usr/bin/env python3
"""Landmine: jidoka SSOT output wired in AGENTS.md (RCA 26-09-25)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_jidoka_ssot_agents_link import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
