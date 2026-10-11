#!/usr/bin/env python3
"""Refuse root-level agent session artifacts (O5)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_root_session_artifacts import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
