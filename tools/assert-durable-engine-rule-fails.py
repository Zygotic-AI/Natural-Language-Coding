#!/usr/bin/env python3
"""Landmine UC13: durable goal without engine.runtime rule."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_durable_engine_rule_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
