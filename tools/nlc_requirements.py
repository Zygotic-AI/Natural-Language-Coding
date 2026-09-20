"""Requirements preflight (ADR 0013). Import or run: python tools/nlc_requirements.py <profile>."""

from __future__ import annotations

import shutil
import sys
from typing import Callable

MIN_PYTHON = (3, 9)


def _missing_python() -> list[str]:
    gaps: list[str] = []
    if sys.version_info < MIN_PYTHON:
        gaps.append(
            f"python>={MIN_PYTHON[0]}.{MIN_PYTHON[1]} (have {sys.version_info.major}.{sys.version_info.minor})"
        )
    return gaps


def _missing_on_path(names: list[str]) -> list[str]:
    return [name for name in names if shutil.which(name) is None]


def preflight(
    *,
    executables: list[str] | None = None,
    need_python: bool = True,
) -> list[str]:
    gaps: list[str] = []
    if need_python:
        gaps.extend(_missing_python())
    if executables:
        gaps.extend(_missing_on_path(executables))
    return gaps


def emit_and_exit(gaps: list[str], hints: list[str] | None = None) -> None:
    if not gaps:
        return
    print("REQUIREMENTS:NOT_MET", file=sys.stderr)
    for g in gaps:
        print(f"  missing: {g}", file=sys.stderr)
    for h in hints or []:
        print(f"  hint: {h}", file=sys.stderr)
    sys.exit(1)


def hub_prove() -> None:
    emit_and_exit(preflight(need_python=True))


def hub_tool() -> None:
    emit_and_exit(preflight(need_python=True))


_PROFILES: dict[str, Callable[[], None]] = {
    "hub_prove": hub_prove,
    "hub_tool": hub_tool,
}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: nlc_requirements.py <profile>", file=sys.stderr)
        print(f"profiles: {', '.join(sorted(_PROFILES))}", file=sys.stderr)
        return 2
    name = sys.argv[1]
    fn = _PROFILES.get(name)
    if fn is None:
        print(f"unknown profile: {name}", file=sys.stderr)
        return 2
    fn()
    print("REQUIREMENTS:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
