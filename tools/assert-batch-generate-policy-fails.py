#!/usr/bin/env python3
"""Landmine ADR 0010: rejected batch-only policy must stay documented as fail-closed."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_batch_generate_policy_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
