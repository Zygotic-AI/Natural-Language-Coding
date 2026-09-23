#!/usr/bin/env python3
"""Build nlc-X.Y.Z.tar.gz for GitHub Releases (maintainer)."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_build import *  # noqa: F403
__all__ = ['EXCLUDE_DIRS', 'ROOT', 'main', 'should_skip']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

