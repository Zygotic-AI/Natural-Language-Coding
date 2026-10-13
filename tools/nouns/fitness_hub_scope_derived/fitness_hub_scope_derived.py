"""C1: hub_material and changed_paths are derived from git, never from the package."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

from nouns.hub_own_produce.hub_own_produce import (
    derive_hub_scope,
    validate_hub_material_package,
)

ROOT = Path(__file__).resolve().parents[3]


def scope_errors(root: Path) -> list[str]:
    """MET when a hub-scope diff forces the hub profile on .nlc/produce-package.json."""
    errors: list[str] = []
    hub, changed = derive_hub_scope(root)
    if "hub_material" in json.loads((root / ".nlc" / "produce-package.json").read_text(encoding="utf-8")):
        # Field may exist; it is never the source of scope. Presence is not an error.
        pass
    if not hub:
        return errors
    if not changed and not (root / "CHARTER.md").is_file():
        errors.append("hub profile mandatory but derived changed_paths empty")
    raw = json.loads((root / ".nlc" / "produce-package.json").read_text(encoding="utf-8"))
    data = {k: v for k, v in raw.items() if not str(k).startswith("_")}
    ok, _kind, reason = validate_hub_material_package(root, data)
    if not ok:
        errors.append(reason)
    return errors


def main() -> int:
    errors = scope_errors(ROOT)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
