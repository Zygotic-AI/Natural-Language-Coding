#!/usr/bin/env python3
"""Landmine ADR 0006: contract_change_blockers catches verify-impact-c21 (non-specimen)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_contract_change_detects_c21_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
