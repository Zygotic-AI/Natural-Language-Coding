#!/usr/bin/env python3
"""Known-bad: clone without v0.3.0 merge-base refs plus a same-actor package must NOT_MET."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.fitness_hub_scope_derived.fitness_hub_scope_derived import scope_errors  # noqa: E402
from nouns.hub_own_produce.hub_own_produce import validate_hub_material_package  # noqa: E402

SAME_ACTOR = ROOT / "tools/fixtures/hub-own/invalid-hub-own-gate-subject-same-actor.json"


def _delete_release_refs(tree: Path) -> None:
    """Hide branch and tag merge-base candidates so merge-base cannot resolve."""
    for ref in (
        "refs/remotes/origin/release/v0.3.0",
        "refs/heads/release/v0.3.0",
        "refs/tags/v0.3.0",
    ):
        subprocess.run(
            ["git", "update-ref", "-d", ref],
            cwd=str(tree),
            check=False,
            capture_output=True,
        )


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td) / "tree"
        subprocess.run(
            ["git", "clone", "--local", str(ROOT), str(tree)],
            check=True,
            capture_output=True,
        )
        _delete_release_refs(tree)
        dest = tree / ".nlc" / "produce-package.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SAME_ACTOR, dest)
        errors = scope_errors(tree)
        raw = json.loads(SAME_ACTOR.read_text(encoding="utf-8"))
        data = {k: v for k, v in raw.items() if not str(k).startswith("_")}
        ok, _kind, reason = validate_hub_material_package(tree, data)
        blob = " ".join(errors + ([] if ok else [reason]))
        if not errors and ok:
            print("ASSERT:FAIL expected NOT_MET for unresolved merge-base, got MET")
            return 1
        if "unresolved merge-base" not in blob:
            print(f"ASSERT:FAIL expected unresolved merge-base in violations, got {blob!r}")
            return 1
        print(f"ASSERT:PASS unresolved merge-base yields NOT_MET ({blob[:160]})")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
