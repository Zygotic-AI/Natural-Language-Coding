#!/usr/bin/env python3
"""Refresh hub-x4-remainder.json classes, counts, and noun_pilots from disk."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.hub_x4_refresh_inventory import hub_x4_refresh_inventory as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
