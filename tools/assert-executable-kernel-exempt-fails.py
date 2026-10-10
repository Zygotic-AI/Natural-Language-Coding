#!/usr/bin/env python3
"""Landmine: the executable-shape kernel cannot exempt its own files."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.executable_shape import exemption_violations


def main() -> int:
    if exemption_violations([]):
        print("ASSERT:FAIL empty exemption list must pass")
        return 1
    hit = exemption_violations(["tools/nouns/executable_shape/executable_shape.py"])
    if not hit:
        print("ASSERT:FAIL kernel path must be refused as an exemption")
        return 1
    print("ASSERT:PASS kernel cannot exempt itself")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
