#!/usr/bin/env python3
"""C6-only ADR ratification. Retired receipts file must stay absent."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.adr_approval import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
