"""Known-good: gate-set membership is computed once per run and reused."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


def main() -> int:
    from nouns.gate_set.gate_set import (
        compute_count,
        derive_gate_set_paths,
        prime_run_cache,
        reset_cache_for_tests,
    )

    os.environ.pop("NLC_GATE_SET_CACHE", None)
    reset_cache_for_tests()
    first = derive_gate_set_paths(ROOT)
    second = derive_gate_set_paths(ROOT)
    if not first:
        return _fail("derive_gate_set_paths returned empty")
    if first != second:
        return _fail("cached membership differed from first compute")
    if compute_count() != 1:
        return _fail(f"expected one compute, got {compute_count()}")

    dest = Path(tempfile.mkdtemp()) / "gate-set-cache.json"
    reset_cache_for_tests()
    prime_run_cache(ROOT, dest)
    primed = compute_count()
    if primed != 1:
        return _fail(f"prime_run_cache should compute once, got {primed}")
    reset_cache_for_tests(process_only=True)
    reused = derive_gate_set_paths(ROOT)
    if compute_count() != primed:
        return _fail(
            f"run cache must prevent a second compute (count {compute_count()} after prime {primed})"
        )
    if reused != first:
        return _fail("run-cache membership differed from first compute")
    print("ASSERT:PASS gate-set membership computed once per run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
