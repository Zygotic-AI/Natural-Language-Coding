#!/usr/bin/env python3
"""NLC distribution: semver, store layout, migrations (ADR 0014, 0015)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.nlc_distribution import nlc_distribution as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})
