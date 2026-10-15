#!/usr/bin/env python3
"""Hub curated pack registry helpers (ADR 0041)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.nlc_pack_registry import nlc_pack_registry as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})
