"""Tag-time checker digest (ADR 0057).

The signed document is one sha256 line. Membership is an explicit rule:
checker programs, the fitness workflow, and numbered architecture decisions.
Examples, generated ledgers, and instruction files are not members.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import re
from pathlib import Path

DIGEST_REL = "integrity/checker-digest.sha256"
ARMOR_REL = DIGEST_REL + ".approval.asc"

_ADR = re.compile(r"^adrs/[0-9]{4}-[^/]+\.md$")
_FITNESS_PY = re.compile(r"^tools/fitness-[^/]+\.py$")
_ASSERT_PY = re.compile(r"^tools/assert-[^/]+\.py$")
_NOUN_PREFIXES = (
    "tools/nouns/ci_fitness/",
    "tools/nouns/verify/",
    "tools/nouns/gate_set/",
    "tools/nouns/gate_set_manifest/",
    "tools/nouns/owner_sidecar/",
    "tools/nouns/nlc_release_tag_gate/",
    "tools/nouns/release_audit/",
    "tools/nouns/checker_digest/",
    "tools/nouns/fitness_adr_owner_sidecar/",
    "tools/nouns/fitness_gate_set_manifest/",
    "tools/nouns/fitness_derived_release_state/",
    "tools/nouns/mandated_paths/",
    "tools/nouns/self_ref_set/",
    "tools/nouns/evidence_ref/",
    "tools/nouns/install_hash_update/",
)
_EXACT = frozenset(
    {
        "tools/ci_fitness.py",
        "tools/nlc.py",
        "tools/check-checker-digest-signature.py",
        "tools/regen-derived-release-state.py",
        "tools/generate-gate-set-baseline-manifest.py",
        ".github/workflows/fitness.yml",
    }
)


def is_checker_digest_path(rel: str) -> bool:
    """True when rel is a pass/fail input in the tag-time signed set."""
    path = rel.replace("\\", "/").lstrip("./")
    if path in _EXACT:
        return True
    if _ADR.match(path) or _FITNESS_PY.match(path) or _ASSERT_PY.match(path):
        return True
    return any(path.startswith(prefix) and path.endswith(".py") for prefix in _NOUN_PREFIXES)


def digest_paths(root: Path) -> list[str]:
    found: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if is_checker_digest_path(rel):
            found.add(rel)
    # pathlib rglob does not enter dot-directories such as .github.
    for rel in _EXACT:
        if (root / rel).is_file():
            found.add(rel)
    return sorted(found)


def _sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def canonical_listing(root: Path) -> bytes:
    lines: list[str] = []
    for rel in digest_paths(root):
        lines.append(f"{rel} {_sha256((root / rel).read_bytes())}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def digest_hex(root: Path) -> str:
    return _sha256(canonical_listing(root))


def digest_file_bytes(root: Path) -> bytes:
    return (digest_hex(root) + "\n").encode("utf-8")


def write_digest(root: Path) -> Path:
    dest = root / DIGEST_REL
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(digest_file_bytes(root))
    return dest


def digest_errors(root: Path) -> list[str]:
    """Byte match only. Armor is not a branch requirement."""
    path = root / DIGEST_REL
    if not path.is_file():
        return [f"missing {DIGEST_REL}"]
    expected = digest_file_bytes(root)
    if path.read_bytes() != expected:
        return [
            f"{DIGEST_REL}: bytes do not match checker listing "
            f"(file {path.read_text(encoding='utf-8').strip()} vs {expected.decode().strip()})"
        ]
    return []
