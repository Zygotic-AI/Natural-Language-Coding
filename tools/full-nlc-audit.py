#!/usr/bin/env python3
"""Full NLC audit — single machine entrypoint (manifest + continuity blockers)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.full_nlc_audit import full_nlc_audit as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
