#!/usr/bin/env python3
"""Landmine UC3/pack consume: bind_ready + requirements-sync-pending blocked."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_requirements_sync_pending_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
