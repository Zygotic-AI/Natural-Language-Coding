#!/usr/bin/env python3
"""Wire X1/X2/X3 into the PLANIT pipeline (ADR 0024 / 0030)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.nlc_pipeline_wire import nlc_pipeline_wire as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
