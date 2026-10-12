#!/usr/bin/env python3
"""PM offline owner ratification verify (ADR 0052 decision 6).

Verification **code** loads only from the checkout containing this script
(Path(__file__).resolve().parents[1]). The --tree argument is **read-only**
data (manifest, ADRs, sidecars, file bytes); it is never added to sys.path.

Uses ONLY the operator-supplied public key and explicit trusted fingerprints.
Does not read integrity/owner-keys/* from --tree for trust decisions.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# SSOT checkout for imports (pinned snapshot the PM runs); not --tree.
TOOL_ROOT = Path(__file__).resolve().parents[1]
if str(TOOL_ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(TOOL_ROOT / "tools"))

from nouns.adr_approval.adr_approval import active_numbers
from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL, manifest_bytes
from nouns.owner_sidecar.owner_sidecar import (
    normalize_fingerprint,
    sidecar_path_for_document,
    verify_sidecar_with_trusted_set,
)

_STATUS = re.compile(r"^-\s*Status:\s*(\S+)", re.M)


def _adr_path(data_root: Path, number: str) -> Path | None:
    matches = sorted((data_root / "adrs").glob(f"{number}-*.md"))
    return matches[0] if len(matches) == 1 else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline owner sidecar verification")
    parser.add_argument(
        "--tree",
        type=Path,
        default=Path("."),
        help="Repository root to read documents from (never used for Python imports)",
    )
    parser.add_argument("--pubkey", type=Path, required=True, help="Operator-owned public key (armored)")
    parser.add_argument(
        "--trusted-fingerprint",
        action="append",
        required=True,
        help="Fingerprint allowed to sign (repeatable; hex, no spaces required)",
    )
    args = parser.parse_args()
    data_root = args.tree.resolve()
    trusted = {normalize_fingerprint(fp) for fp in args.trusted_fingerprint}
    key_paths = [args.pubkey.resolve()]
    violations: list[str] = []

    manifest_path = data_root / MANIFEST_REL
    if not manifest_path.is_file():
        violations.append(f"missing {MANIFEST_REL}")
    else:
        if manifest_path.read_bytes() != manifest_bytes(data_root):
            violations.append(f"{MANIFEST_REL} bytes do not match tree gate-set")
        asc = data_root / sidecar_path_for_document(MANIFEST_REL)
        violations.extend(
            verify_sidecar_with_trusted_set(
                data_root,
                MANIFEST_REL,
                asc,
                trusted_fingerprints=trusted,
                key_import_paths=key_paths,
            )
        )

    active = data_root / "adrs" / "ACTIVE.md"
    if not active.is_file():
        violations.append("missing adrs/ACTIVE.md")
    else:
        for number in active_numbers(active.read_text(encoding="utf-8")):
            if int(number) <= 51:
                continue
            path = _adr_path(data_root, number)
            if path is None:
                violations.append(f"ADR {number}: missing file")
                continue
            text = path.read_text(encoding="utf-8")
            status_match = _STATUS.search(text)
            if status_match and status_match.group(1) != "Accepted":
                continue
            rel = str(path.relative_to(data_root)).replace("\\", "/")
            asc = data_root / sidecar_path_for_document(rel)
            violations.extend(
                verify_sidecar_with_trusted_set(
                    data_root,
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
