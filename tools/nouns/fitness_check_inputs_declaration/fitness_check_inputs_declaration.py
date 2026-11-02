"""Every labeled check must declare inputs; committed map must match derivation."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.check_inputs.check_inputs import declaration_errors  # noqa: E402


def empty_inputs_are_refused() -> bool:
    """True when a check with no own files is treated as lacking a declaration."""
    from nouns.check_inputs.check_inputs import CheckDecl, declared_inputs

    ghost = CheckDecl("ghost-check-no-inputs", "tools/does-not-exist-check.py", "fitness")
    return declared_inputs(ROOT, ghost) == []


def main() -> int:
    _ = sys.argv[1:]
    errors = declaration_errors(ROOT)
    if not empty_inputs_are_refused():
        errors.append("missing-declaration fixture did not refuse")
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
