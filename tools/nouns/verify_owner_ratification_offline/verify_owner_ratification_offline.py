"""PM offline owner ratification verify (ADR 0052 decision 6)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import re
import sys
from pathlib import Path

from nouns.adr_approval.adr_approval import active_numbers
from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL, manifest_bytes
from nouns.owner_sidecar.owner_sidecar import (
    normalize_fingerprint,
    sidecar_path_for_document,
    verify_sidecar_with_trusted_set,
)

_STATUS = re.compile(r"^-\s*Status:\s*(\S+)", re.M)


def tool_root_from_adapter(adapter_path: Path) -> Path:
    """Repo root containing the tools/ tree for imports (not --tree)."""
    return adapter_path.resolve().parents[1]


def _adr_path(data_root: Path, number: str) -> Path | None:
    matches = sorted((data_root / "adrs").glob(f"{number}-*.md"))
    return matches[0] if len(matches) == 1 else None


def run_offline_verify(
    *,
    data_root: Path,
    pubkey: Path,
    trusted_fingerprints: set[str],
) -> list[str]:
    violations: list[str] = []
    key_paths = [pubkey.resolve()]

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
                trusted_fingerprints=trusted_fingerprints,
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
                    trusted_fingerprints=trusted_fingerprints,
                    key_import_paths=key_paths,
                )
            )
    return violations


def main(argv: list[str] | None = None, *, adapter_path: Path | None = None) -> int:
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
    args = parser.parse_args(argv)
    if adapter_path is not None:
        tool_root = tool_root_from_adapter(adapter_path)
        if str(tool_root / "tools") not in sys.path:
            sys.path.insert(0, str(tool_root / "tools"))

    data_root = args.tree.resolve()
    trusted = {normalize_fingerprint(fp) for fp in args.trusted_fingerprint}
    violations = run_offline_verify(
        data_root=data_root,
        pubkey=args.pubkey,
        trusted_fingerprints=trusted,
    )
    if violations:
        for item in violations:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0
