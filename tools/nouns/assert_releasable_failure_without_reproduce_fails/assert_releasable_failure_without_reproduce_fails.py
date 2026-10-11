"""Landmine: gate failures must print Reproduce (RCA-1 C2)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import io
import sys
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.releasable_gates import releasable_gates as rg

    buf = io.StringIO()
    with redirect_stderr(buf):
        rg.emit_gate_failure("fixture-gate", "./nlc gate fixture-gate --tree .", ROOT)
    text = buf.getvalue()
    if "Reproduce:" not in text:
        print("ASSERT:FAIL emit_gate_failure must print Reproduce:")
        print(text)
        return 1
    source = (ROOT / "tools" / "nouns" / "releasable_gates" / "releasable_gates.py").read_text(
        encoding="utf-8"
    )
    if "Reproduce:" not in source:
        print("ASSERT:FAIL releasable_gates.py missing Reproduce emitter")
        return 1
    verify = (ROOT / "tools" / "nouns" / "verify" / "verify.py").read_text(encoding="utf-8")
    if "/verify in your agent" in verify.lower():
        print("ASSERT:FAIL verify.py still redirects to agent prose")
        return 1
    print("ASSERT:PASS gate failures require Reproduce command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
