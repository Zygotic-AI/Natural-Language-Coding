"""ADR 0018 interview-shaped CLI gaps (human stderr; optional machine line last)."""

from __future__ import annotations

import sys

BOUNDARY = "bba-emit"


def emit_gap(
    problem: str,
    *,
    missing: list[str] | None = None,
    ask: str | None = None,
    choices: list[str] | None = None,
    examples: list[str] | None = None,
    machine: str | None = "NLC:NOT_MET",
) -> int:
    print(problem, file=sys.stderr)
    for line in missing or []:
        print(f"  What's wrong: {line}", file=sys.stderr)
    if ask:
        print(f"  {ask}", file=sys.stderr)
    for c in choices or []:
        print(f"  Option: {c}", file=sys.stderr)
    for ex in examples or []:
        print(f"  Example: {ex}", file=sys.stderr)
    if machine:
        print(machine, file=sys.stderr)
    return 2
