"""Fitness: committed hub before-generate stamp carries every SSOT scope."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import stat
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HUB_STAMP_SCOPES_INPUT = "integrity/hub-stamp-scopes.json"
HUB_STAMP_INPUT = ".nlc/before-generate-stamp.json"
sys.path.insert(0, str(ROOT / "tools"))

from nouns.hub_stamp_scopes.hub_stamp_scopes import (  # noqa: E402
    HUB_STAMP_REL,
    HUB_STAMP_SCOPES_REL,
    load_scopes_file,
    stamp_check_errors,
    stamp_scope_gap_errors,
)

FIXTURES = ROOT / "tools" / "fixtures" / "hub-stamp-scopes"
EMPTY_SOURCE = FIXTURES / "empty-scopes-source.json"
PARTIAL_STAMP = FIXTURES / "partial-stamp-scopes.json"


def _source_fail_closed_cases() -> list[str]:
    errors: list[str] = []
    missing = FIXTURES / "does-not-exist-scopes.json"
    _scopes, err = load_scopes_file(missing)
    if err != "missing hub stamp scopes source":
        errors.append("missing source file must fail closed")
    if not EMPTY_SOURCE.is_file():
        errors.append(f"missing fixture {EMPTY_SOURCE.relative_to(ROOT)}")
    else:
        _scopes, err = load_scopes_file(EMPTY_SOURCE)
        if err != "empty hub stamp scopes source":
            errors.append("empty source file must fail closed")
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        handle.write('{"scopes":["default"]}')
        unreadable = Path(handle.name)
    try:
        unreadable.chmod(0)
        _scopes, err = load_scopes_file(unreadable)
        if err != "unreadable hub stamp scopes source":
            errors.append("unreadable source file must fail closed")
    finally:
        unreadable.chmod(stat.S_IWUSR | stat.S_IRUSR)
        unreadable.unlink(missing_ok=True)
    return errors


def _stamp_gap_case() -> str | None:
    if not PARTIAL_STAMP.is_file():
        return f"missing fixture {PARTIAL_STAMP.relative_to(ROOT)}"
    required, err = load_scopes_file(ROOT / HUB_STAMP_SCOPES_REL)
    if err or not required:
        return "hub SSOT scopes unreadable for fixture test"
    import json

    stamp_scopes = json.loads(PARTIAL_STAMP.read_text(encoding="utf-8")).get("scopes") or []
    gap = stamp_scope_gap_errors(required, stamp_scopes)
    if not gap:
        return "partial stamp fixture must NOT_MET"
    return None


def main() -> int:
    _ = sys.argv[1:]
    errors = stamp_check_errors(ROOT)
    errors.extend(_source_fail_closed_cases())
    gap = _stamp_gap_case()
    if gap:
        errors.append(gap)
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
