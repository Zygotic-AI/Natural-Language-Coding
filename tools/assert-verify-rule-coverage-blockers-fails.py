#!/usr/bin/env python3
"""Landmine ADR 0023: verify_fast includes rule-coverage blocker on missing markers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_rule_coverage_blockers_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
