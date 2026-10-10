#!/usr/bin/env python3
"""UC requirement packs v0.2: ingest source → candidate ADRs/rules (human ratifies)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.nlc_pack_ingest import nlc_pack_ingest as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
