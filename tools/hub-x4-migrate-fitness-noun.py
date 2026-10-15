#!/usr/bin/env python3
"""Move fitness-*.py interiors into tools/nouns/<slug>/ with thin adapters (X4 t4)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.hub_x4_migrate_fitness_noun import hub_x4_migrate_fitness_noun as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
