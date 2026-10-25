#!/usr/bin/env python3
"""Write integrity/planit-skill-registry.json from canonical Planit skill bytes."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.planit_identity.planit_identity import write_registry_from_bytes


def main() -> int:
    root = Path.cwd()
    dest = write_registry_from_bytes(root)
    print(f"wrote {dest.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
