"""Converge integrity/hub-content-tree-hash.txt (content digest excluding that file)."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_TOOLS = Path(__file__).resolve().parents[2]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from nouns.gate_set.gate_set import (  # noqa: E402
    BOOTSTRAP_ARMOR_REL,
    BOOTSTRAP_STATEMENT_REL,
    MANIFEST_APPROVAL_ASC_REL,
    armor_occupancy_paths,
)

HASH_REL = "integrity/hub-content-tree-hash.txt"
PLANIT_EVIDENCE_REL = ".nlc/planit-change-evidence.json"
MANIFEST_REL = "integrity/gate-set-baseline.manifest.sha256"
HASH_PATH = ROOT / HASH_REL


def _content_exclude_rel() -> set[str]:
    """Paths omitted from the hub content digest (self-describing hash + harness stamps)."""
    # The exclusion breaks a hash cycle.
    return {
        HASH_REL,
        PLANIT_EVIDENCE_REL,
        MANIFEST_REL,
        MANIFEST_APPROVAL_ASC_REL,
        BOOTSTRAP_STATEMENT_REL,
        BOOTSTRAP_ARMOR_REL,
        *armor_occupancy_paths(),
    }


def content_digest_excluding(root: Path, exclude_rel: set[str]) -> str:
    """
    SHA-256 over sorted tracked paths and bytes (ADR 0050 content fingerprint).

    Excluded paths are omitted entirely so the hash file can self-describe.
    """
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return ""
    digest = hashlib.sha256()
    for rel in sorted(line.strip() for line in (proc.stdout or "").splitlines() if line.strip()):
        if rel in exclude_rel:
            continue
        path = root / rel
        if not path.is_file():
            continue
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def sync_content_tree_hash(root: Path | None = None) -> str:
    """Write hub-content-tree-hash.txt to the current content digest (single step)."""
    base = root or ROOT
    path = base / HASH_REL
    h = content_digest_excluding(base, _content_exclude_rel())
    if not h:
        raise RuntimeError("cannot compute hub content digest")
    if read_content_tree_hash(base) == h:
        return h
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(h + "\n", encoding="utf-8")
    return h


def read_content_tree_hash(root: Path | None = None) -> str:
    """Return recorded hub content digest or empty string."""
    base = root or ROOT
    path = base / HASH_REL
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip().lower()


def verify_content_tree_hash(root: Path | None = None) -> tuple[bool, str, str]:
    """Return (ok, recorded, expected) for the content fingerprint."""
    base = root or ROOT
    recorded = read_content_tree_hash(base)
    expected = content_digest_excluding(base, _content_exclude_rel()).lower()
    if not recorded or not expected:
        return False, recorded, expected
    return recorded == expected, recorded, expected


def main() -> int:
    try:
        h = sync_content_tree_hash()
    except RuntimeError as exc:
        print(f"SYNC:REFUSE {exc}", file=sys.stderr)
        return 2
    print(f"SYNC:MET digest={h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
