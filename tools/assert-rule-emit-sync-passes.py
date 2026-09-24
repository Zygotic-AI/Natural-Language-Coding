#!/usr/bin/env python3
"""Landmine ADR 0023: rule-emit inserts missing nlc:rule= markers on generate."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_rule_emit_sync_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
