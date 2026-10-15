#!/usr/bin/env python3
"""ADR 0023: scan nlc:rule=<id> markers; map ADR/tag → enforcement sites (CLI adapter)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.nlc_rule_coverage import nlc_rule_coverage as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
