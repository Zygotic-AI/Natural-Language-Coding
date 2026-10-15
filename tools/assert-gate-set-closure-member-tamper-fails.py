#!/usr/bin/env python3
"""Landmine: tampering a closure member must NOT_MET gate-set manifest fitness."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.gate_set_manifest.gate_set_manifest import gate_set_manifest_errors  # noqa: E402


def _check_tamper(rel: str) -> int:
    path = ROOT / rel
    if not path.is_file():
        print(f"ASSERT:FAIL missing {rel}")
        return 1
    tampered = path.read_bytes() + b"# tamper\n"
    errors = gate_set_manifest_errors(ROOT, overrides={rel: tampered})
    if not errors:
        print(f"ASSERT:FAIL tamper on {rel} expected NOT_MET got MET")
        return 1
    print(f"ASSERT:PASS tamper on {rel} yields NOT_MET ({errors[0]})")
    return 0


def main() -> int:
    if len(sys.argv) == 2:
        rels = [sys.argv[1].replace("\\", "/").lstrip("./")]
    elif len(sys.argv) == 1:
        rels = [
            "tools/nouns/release_state/release_state.py",
            "tools/nouns/nlc_requirements/__init__.py",
        ]
    else:
        print("usage: assert-gate-set-closure-member-tamper-fails.py [<repo-relative-path>]")
        return 2
    for rel in rels:
        code = _check_tamper(rel)
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
