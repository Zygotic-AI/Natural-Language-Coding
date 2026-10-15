#!/usr/bin/env python3
"""Validate integrity/hub-pack-registry.json (ADR 0041 v1)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.validate_hub_pack_registry import validate_hub_pack_registry as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
