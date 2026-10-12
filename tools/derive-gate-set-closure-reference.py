#!/usr/bin/env python3
"""v2. Derive the NLC gate set = transitive load closure of everything CI runs.

Usage: derive-gate-set-closure-reference.py <repo-root>   -> prints sorted repo-relative paths.

Reference algorithm (PM closure v2). SSOT implementation: nouns.gate_set.gate_set.derive_gate_set_paths.

Also excludes exactly (not by pattern): integrity/gate-set-baseline.manifest.sha256.approval.asc
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "tools"))
from nouns.gate_set.gate_set import MANIFEST_APPROVAL_ASC_REL, derive_gate_set_paths  # noqa: E402

assert MANIFEST_APPROVAL_ASC_REL == "integrity/gate-set-baseline.manifest.sha256.approval.asc"

if __name__ == "__main__":
    print("\n".join(derive_gate_set_paths(ROOT)))
