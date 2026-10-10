#!/usr/bin/env python3
"""Resolve hub tool source text (thin adapter vs noun implementation)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_source import fitness_hub_source as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})
