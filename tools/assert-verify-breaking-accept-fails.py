#!/usr/bin/env python3
"""Landmine: breaking contract with ADR but no acceptance must fail verify (ADR 0006)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_breaking_accept_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
