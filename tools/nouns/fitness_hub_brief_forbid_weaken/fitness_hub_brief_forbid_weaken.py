"""C3: hub material brief_ref names every property leaf and the forbid clause."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

from nouns.hub_own_produce.hub_own_produce import derive_hub_scope, validate_hub_brief

ROOT = Path(__file__).resolve().parents[3]
MISSING_CLAUSE = ROOT / "tools/fixtures/hub-brief/missing-forbid-clause.json"
MISSING_LEAF = ROOT / "tools/fixtures/hub-brief/missing-leaf-id.json"


def brief_errors(root: Path) -> list[str]:
    errors: list[str] = []
    hub, _changed = derive_hub_scope(root)
    if hub:
        raw = json.loads((root / ".nlc" / "produce-package.json").read_text(encoding="utf-8"))
        data = {k: v for k, v in raw.items() if not str(k).startswith("_")}
        ok, reason = validate_hub_brief(root, data)
        if not ok:
            errors.append(reason)
    return errors


def _fixture_must_fail(path: Path, needle: str) -> str | None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data = {k: v for k, v in data.items() if not str(k).startswith("_")}
    ok, reason = validate_hub_brief(ROOT, data)
    if ok:
        return f"{path.name}: expected NOT_MET got MET"
    if needle not in reason:
        return f"{path.name}: expected {needle!r} in {reason!r}"
    return None


def main() -> int:
    errors = brief_errors(ROOT)
    for path, needle in (
        (MISSING_CLAUSE, "forbid clause"),
        (MISSING_LEAF, "leaf id"),
    ):
        if not path.is_file():
            errors.append(f"missing known-bad {path.relative_to(ROOT)}")
            continue
        fail = _fixture_must_fail(path, needle)
        if fail:
            errors.append(fail)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
