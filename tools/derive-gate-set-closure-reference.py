#!/usr/bin/env python3
"""Reference runner: derive gate-set closure (must match closure.txt at repo root).

Usage: derive-gate-set-closure-reference.py <repo-root>
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "tools"))
from nouns.gate_set.gate_set import derive_gate_set_paths  # noqa: E402

if __name__ == "__main__":
    print("\n".join(derive_gate_set_paths(ROOT)))
