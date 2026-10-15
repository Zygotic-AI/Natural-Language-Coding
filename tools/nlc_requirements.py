#!/usr/bin/env python3
"""Requirements preflight (ADR 0013). Import or run: python tools/nlc_requirements.py <profile>."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.nlc_requirements import nlc_requirements as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
