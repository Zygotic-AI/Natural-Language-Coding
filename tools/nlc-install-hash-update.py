#!/usr/bin/env python3
"""Regenerate integrity/nlc-install-hashes.json (maintainer)."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.install_hash_update import *  # noqa: F403
__all__ = ['GLOBS', 'OUT', 'ROOT', 'main', 'sha256_file']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

