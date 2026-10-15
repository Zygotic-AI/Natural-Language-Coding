#!/usr/bin/env python3
"""ADR 0025: validate RCA packet JSON (schema + no-blame climb rules)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.validate_rca_packet import validate_rca_packet as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
