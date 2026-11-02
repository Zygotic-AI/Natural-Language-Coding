"""Known-bad: a file that maps to no check must run the full suite."""

from __future__ import annotations

BOUNDARY = "bba-emit"

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
UNMAPPED = "__unmapped__/no-known-check.txt"


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


def main() -> int:
    from nouns.check_inputs.check_inputs import check_inputs_map, derive_payload
    from nouns.check_selection.check_selection import select_checks

    mapping = check_inputs_map(ROOT, derive_payload(ROOT))
    if UNMAPPED in {rel for inputs in mapping.values() for rel in inputs}:
        return _fail(f"specimen {UNMAPPED} is already mapped")
    sel = select_checks(changed=[UNMAPPED], check_inputs=mapping, mode="pr")
    if not sel.full_suite:
        return _fail("unmapped file narrowed the suite")
    if "unmapped" not in sel.reason:
        return _fail(f"expected unmapped reason, got {sel.reason!r}")
    print("ASSERT:PASS unmapped file change runs the full suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
