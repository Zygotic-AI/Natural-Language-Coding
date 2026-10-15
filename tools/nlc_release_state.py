#!/usr/bin/env python3
"""Observe hub release facts and print the one legal action. Does not mutate git."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.nlc_release_state import nlc_release_state as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    from nlc_requirements import hub_tool
    hub_tool()
    raise SystemExit(main())
