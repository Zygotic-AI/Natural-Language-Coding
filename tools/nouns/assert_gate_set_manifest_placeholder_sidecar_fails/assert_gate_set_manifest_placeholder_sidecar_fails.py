"""Landmine: committed placeholder manifest sidecar must not widen closure or hub digest."""

from __future__ import annotations

BOUNDARY = "bba-emit"

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
from nouns.gate_set.gate_set import MANIFEST_APPROVAL_ASC_REL, derive_gate_set_paths  # noqa: E402
from nouns.gate_set_manifest.gate_set_manifest import (  # noqa: E402
    MANIFEST_REL,
    _manifest_path_set,
    gate_set_manifest_errors,
)


def _manifest_path_column(root: Path) -> list[str]:
    manifest = root / MANIFEST_REL
    return sorted(_manifest_path_set(manifest.read_bytes()))


def main() -> int:
    baseline_paths = _manifest_path_column(ROOT)
    baseline_derive = derive_gate_set_paths(ROOT)
    if baseline_paths != sorted(baseline_derive):
        print("ASSERT:FAIL baseline manifest path column != derive_gate_set_paths")
        return 1
    exclude = _content_exclude_rel()
    baseline_hub = content_digest_excluding(ROOT, exclude).lower()

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
        asc = tree / MANIFEST_APPROVAL_ASC_REL
        asc.parent.mkdir(parents=True, exist_ok=True)
        asc.write_bytes(b"-----BEGIN PGP SIGNED MESSAGE-----\nnot-valid\n")
        subprocess.run(["git", "add", MANIFEST_APPROVAL_ASC_REL], cwd=tree, check=True)

        after_derive = derive_gate_set_paths(tree)
        if after_derive != baseline_derive:
            print(
                "ASSERT:FAIL placeholder sidecar changed derive_gate_set_paths "
                f"(was {len(baseline_derive)}, now {len(after_derive)})"
            )
            return 1
        if _manifest_path_column(tree) != baseline_paths:
            print("ASSERT:FAIL placeholder sidecar changed manifest path column")
            return 1
        after_hub = content_digest_excluding(tree, exclude).lower()
        if after_hub != baseline_hub:
            print(
                f"ASSERT:FAIL placeholder sidecar changed hub digest ({baseline_hub} -> {after_hub})"
            )
            return 1

        errors = gate_set_manifest_errors(tree)
        if not errors:
            print("ASSERT:FAIL placeholder sidecar expected NOT_MET got MET")
            return 1
        if any("missing sidecar" in e for e in errors):
            print(f"ASSERT:FAIL expected signature failure not missing sidecar: {errors!r}")
            return 1
        if any("bytes do not match" in e for e in errors):
            print(f"ASSERT:FAIL unexpected bytes mismatch: {errors!r}")
            return 1
        if any("missing" in e and "derived gate-set" in e for e in errors):
            print(f"ASSERT:FAIL unexpected path-set mismatch: {errors!r}")
            return 1
        if any("extra path" in e for e in errors):
            print(f"ASSERT:FAIL unexpected extra paths: {errors!r}")
            return 1
        sig_errors = errors

    print(f"ASSERT:PASS placeholder sidecar NOT_MET on signature only ({sig_errors[0]})")
    return 0
