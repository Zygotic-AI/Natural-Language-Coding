"""Landmine: fitness hub stamp scope SSOT missing or unreadable sources fail closed."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import stat
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.hub_stamp_scopes.hub_stamp_scopes import load_scopes_file  # noqa: E402

FIXTURES = ROOT / "tools" / "fixtures" / "hub-stamp-scopes"
EMPTY = FIXTURES / "empty-scopes-source.json"


def main() -> int:
    missing = FIXTURES / "does-not-exist-scopes.json"
    _scopes, err = load_scopes_file(missing)
    if err != "missing hub stamp scopes source":
        print("ASSERT:FAIL missing SSOT must fail closed")
        return 1
    if not EMPTY.is_file():
        print("ASSERT:FAIL missing empty SSOT fixture")
        return 1
    _scopes, err = load_scopes_file(EMPTY)
    if err != "empty hub stamp scopes source":
        print("ASSERT:FAIL empty SSOT must fail closed")
        return 1
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        handle.write('{"scopes":["default"]}')
        unreadable = Path(handle.name)
    try:
        unreadable.chmod(0)
        _scopes, err = load_scopes_file(unreadable)
        if err != "unreadable hub stamp scopes source":
            print("ASSERT:FAIL unreadable SSOT must fail closed")
            return 1
    finally:
        unreadable.chmod(stat.S_IWUSR | stat.S_IRUSR)
        unreadable.unlink(missing_ok=True)
    print("ASSERT:PASS hub stamp scope SSOT fail closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
