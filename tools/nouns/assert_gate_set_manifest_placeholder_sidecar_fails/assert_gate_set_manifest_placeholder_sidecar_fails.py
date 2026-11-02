"""Landmine: placeholder armor at every occupancy path must not widen closure or hub digest.

Signing order: place placeholder (or real) armor at every path
`armor_occupancy_paths()` returns *before* write_verified, content-tree
sync, and remanifest. A dry-run that only touches the excluded manifest
sidecar misses occupancy paths that are live digest members.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.evidence_ref.sync_content_tree_hash import (  # noqa: E402
    _content_exclude_rel,
    content_digest_excluding,
)
from nouns.gate_set.gate_set import (  # noqa: E402
    armor_occupancy_paths,
    derive_gate_set_paths,
    place_placeholder_armor,
    reset_cache_for_tests,
)
from nouns.gate_set_manifest.gate_set_manifest import (  # noqa: E402
    MANIFEST_REL,
    _manifest_path_set,
    gate_set_manifest_errors,
)


def _manifest_path_column(root: Path) -> list[str]:
    manifest = root / MANIFEST_REL
    return sorted(_manifest_path_set(manifest.read_bytes()))


def main() -> int:
    occupancy = list(armor_occupancy_paths())
    if not occupancy:
        print("ASSERT:FAIL armor_occupancy_paths is empty")
        return 1
    baseline_paths = _manifest_path_column(ROOT)
    baseline_derive = derive_gate_set_paths(ROOT)
    if baseline_paths != sorted(baseline_derive):
        print("ASSERT:FAIL baseline manifest path column != derive_gate_set_paths")
        return 1
    exclude = _content_exclude_rel()

    with tempfile.TemporaryDirectory() as td:
        tree = Path(td) / "tree"
        subprocess.run(
            ["git", "clone", "--local", str(ROOT), str(tree)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "bash",
                "-c",
                f"cd {ROOT} && tar cf - --exclude=.git . | (cd {tree} && tar xf -)",
            ],
            check=True,
        )
        added = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "-z", "--diff-filter=A"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        )
        names = [n for n in added.stdout.decode().split("\0") if n]
        if names:
            subprocess.run(["git", "add", "--", *names], cwd=tree, check=True)
        saved_cache = os.environ.pop("NLC_GATE_SET_CACHE", None)
        reset_cache_for_tests()
        before_derive = derive_gate_set_paths(tree)
        before_hub = content_digest_excluding(tree, exclude).lower()
        placed = place_placeholder_armor(tree)
        if sorted(placed) != sorted(occupancy):
            print(f"ASSERT:FAIL occupancy {occupancy!r} != placed {placed!r}")
            return 1
        for rel in placed:
            subprocess.run(["git", "add", rel], cwd=tree, check=True)

        reset_cache_for_tests()
        after_derive = derive_gate_set_paths(tree)
        if saved_cache is not None:
            os.environ["NLC_GATE_SET_CACHE"] = saved_cache
        reset_cache_for_tests()
        if after_derive != before_derive:
            print(
                "ASSERT:FAIL placeholder occupancy changed derive_gate_set_paths "
                f"(was {len(before_derive)}, now {len(after_derive)})"
            )
            return 1
        if _manifest_path_column(tree) != baseline_paths:
            print("ASSERT:FAIL placeholder occupancy changed manifest path column")
            return 1
        after_hub = content_digest_excluding(tree, exclude).lower()
        if after_hub != before_hub:
            print(
                f"ASSERT:FAIL placeholder occupancy changed hub digest ({before_hub} -> {after_hub})"
            )
            return 1

        errors = gate_set_manifest_errors(tree)
        if errors:
            print(f"ASSERT:FAIL placeholder armor failed the branch suite: {errors!r}")
            return 1

    print("ASSERT:PASS placeholder armor does not fail the branch suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
