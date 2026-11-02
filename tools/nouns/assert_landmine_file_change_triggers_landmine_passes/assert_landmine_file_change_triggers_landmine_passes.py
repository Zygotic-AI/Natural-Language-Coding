"""Known-good: changing a landmine's own file selects that landmine check."""

from __future__ import annotations

BOUNDARY = "bba-emit"

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


def main() -> int:
    from nouns.check_inputs.check_inputs import check_inputs_map, derive_payload, discover_checks
    from nouns.check_selection.check_selection import select_checks

    payload = derive_payload(ROOT)
    mapping = check_inputs_map(ROOT, payload)
    landmines = [row for row in discover_checks(ROOT) if row.kind == "landmine"]
    if not landmines:
        return _fail("no landmine checks discovered")
    target = None
    for row in landmines:
        inputs = mapping.get(row.label) or []
        if inputs:
            target = (row, inputs[0])
            break
    if target is None:
        return _fail("landmine lacks declared inputs")
    row, rel = target
    sel = select_checks(changed=[rel], check_inputs=mapping, mode="pr")
    if sel.full_suite:
        return _fail(f"landmine file {rel} fell back to full suite: {sel.reason}")
    if row.label not in sel.selected:
        return _fail(f"landmine {row.label} not selected for {rel}")
    print(f"ASSERT:PASS landmine file {rel} triggers {row.label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
