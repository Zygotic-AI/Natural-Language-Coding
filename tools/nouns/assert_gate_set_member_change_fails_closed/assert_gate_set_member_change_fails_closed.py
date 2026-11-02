"""Known-bad: a real gate-set member edit must fail closed.

Missing tool, empty result, or unknown result counts as false (not a pass).
A content-only / hash-stamp edit is not this case (see the content-only pass).
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

MEMBER_REL = "tools/nouns/release_state/release_state.py"


def _as_fail_closed(value: object, *, label: str) -> bool:
    """True only when the check produced a known non-empty failure list."""
    if value is None:
        print(f"ASSERT:FAIL {label}: missing tool or None result counts as false")
        return False
    if value is False:
        print(f"ASSERT:FAIL {label}: unknown/false result counts as false")
        return False
    if value == "" or value == [] or value == ():
        print(f"ASSERT:FAIL {label}: empty result counts as false")
        return False
    if not isinstance(value, list):
        print(f"ASSERT:FAIL {label}: unknown result type {type(value).__name__} counts as false")
        return False
    return True


def main() -> int:
    member = ROOT / MEMBER_REL
    if not member.is_file():
        print(f"ASSERT:FAIL missing real gate-set file {MEMBER_REL}")
        return 1
    try:
        from nouns.gate_set.gate_set import derive_gate_set_paths
        from nouns.gate_set_manifest.gate_set_manifest import gate_set_manifest_errors
    except Exception as exc:
        print(f"ASSERT:FAIL missing tool (import failed): {exc}")
        return 1

    try:
        derived = derive_gate_set_paths(ROOT)
    except Exception as exc:
        print(f"ASSERT:FAIL derive_gate_set_paths missing or failed: {exc}")
        return 1
    if not _as_fail_closed(derived, label="derive_gate_set_paths"):
        return 1
    if MEMBER_REL not in derived:
        print(f"ASSERT:FAIL {MEMBER_REL} is not a derived gate-set member")
        return 1

    tampered = member.read_bytes() + b"# gate-set member tamper\n"
    try:
        errors = gate_set_manifest_errors(ROOT, overrides={MEMBER_REL: tampered})
    except Exception as exc:
        print(f"ASSERT:FAIL gate_set_manifest_errors missing or failed: {exc}")
        return 1
    if not _as_fail_closed(errors, label="gate_set_manifest_errors"):
        return 1
    print(
        "ASSERT:PASS real gate-set member edit fails closed "
        f"({errors[0]})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
