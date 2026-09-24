#!/usr/bin/env python3
"""Landmine ADR 0012: rule-adoption-conflict specimen must ADOPTION:NOT_MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_rule_adoption_conflicts_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
