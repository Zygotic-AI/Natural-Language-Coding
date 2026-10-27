"""Known-bad: a selection error or unreadable map must run the full suite."""

from __future__ import annotations

BOUNDARY = "bba-emit"

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


def main() -> int:
    from nouns.check_inputs.check_inputs import check_inputs_map, derive_payload
    from nouns.check_selection.check_selection import select_checks

    mapping = check_inputs_map(ROOT, derive_payload(ROOT))
    err = select_checks(changed=["README.md"], check_inputs=mapping, mode="pr", error="boom")
    if not err.full_suite or "selection error" not in err.reason:
        return _fail(f"error did not force full suite: {err.reason!r}")
    unread = select_checks(changed=["README.md"], check_inputs=None, mode="pr")
    if not unread.full_suite or "unreadable" not in unread.reason:
        return _fail(f"unreadable map did not force full suite: {unread.reason!r}")
    missing = select_checks(changed=None, check_inputs=mapping, mode="pr")
    if not missing.full_suite or "selection error" not in missing.reason:
        return _fail(f"missing changed files did not force full suite: {missing.reason!r}")
    print("ASSERT:PASS selection error runs the full suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
