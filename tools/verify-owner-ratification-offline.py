#!/usr/bin/env python3
"""PM offline owner ratification verify (ADR 0052 decision 6).

Uses ONLY the operator-supplied public key file and explicit trusted fingerprints.
Does not read integrity/owner-keys/* from the tree for trust decisions.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.adr_approval.adr_approval import active_numbers
from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL, gate_set_manifest_errors
from nouns.owner_sidecar.owner_sidecar import (
    REPO_SLUG,
    load_trusted_fingerprints_from_text,
    normalize_fingerprint,
    sidecar_path_for_document,
    verify_sidecar_p1_fields,
    verify_sidecar_with_trusted_set,
    gpg_verify_clearsigned,
    _document_requires_status_line,
    _status_line_errors,
)
from nouns.gate_set_manifest.gate_set_manifest import manifest_bytes

_STATUS = re.compile(r"^-\s*Status:\s*(\S+)", re.M)


def _adr_path(root: Path, number: str) -> Path | None:
    matches = sorted((root / "adrs").glob(f"{number}-*.md"))
    return matches[0] if len(matches) == 1 else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline owner sidecar verification")
    parser.add_argument("--tree", type=Path, default=Path("."), help="Repository root")
    parser.add_argument("--pubkey", type=Path, required=True, help="Operator-owned public key (armored)")
    parser.add_argument(
        "--trusted-fingerprint",
        action="append",
        required=True,
        help="Fingerprint allowed to sign (repeatable; hex, no spaces required)",
    )
    args = parser.parse_args()
    root = args.tree.resolve()
    trusted = {normalize_fingerprint(fp) for fp in args.trusted_fingerprint}
    key_paths = [args.pubkey.resolve()]
    violations: list[str] = []

    # Gate-set manifest bytes + sidecar
    manifest_path = root / MANIFEST_REL
    if not manifest_path.is_file():
        violations.append(f"missing {MANIFEST_REL}")
    else:
        if manifest_path.read_bytes() != manifest_bytes(root):
            violations.append(f"{MANIFEST_REL} bytes do not match tree gate-set")
        asc = root / sidecar_path_for_document(MANIFEST_REL)
        violations.extend(
            verify_sidecar_with_trusted_set(
                root,
                MANIFEST_REL,
                asc,
                trusted_fingerprints=trusted,
                key_import_paths=key_paths,
            )
        )

    # Accepted ADRs > 0051
    for number in active_numbers((root / "adrs" / "ACTIVE.md").read_text(encoding="utf-8")):
        if int(number) <= 51:
            continue
        path = _adr_path(root, number)
        if path is None:
            violations.append(f"ADR {number}: missing file")
            continue
        text = path.read_text(encoding="utf-8")
        if _STATUS.search(text) and _STATUS.search(text).group(1) != "Accepted":
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        asc = root / sidecar_path_for_document(rel)
        violations.extend(
            verify_sidecar_with_trusted_set(
                root,
                rel,
                asc,
                trusted_fingerprints=trusted,
                key_import_paths=key_paths,
            )
        )

    if violations:
        for item in violations:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
