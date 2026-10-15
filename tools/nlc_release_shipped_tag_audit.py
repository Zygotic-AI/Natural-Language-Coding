#!/usr/bin/env python3
"""ADR 0040: last shipped tag must pass release tag gate (static); print remediation."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.nlc_release_shipped_tag_audit import nlc_release_shipped_tag_audit as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
