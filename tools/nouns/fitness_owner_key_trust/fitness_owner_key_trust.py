"""ADR 0052 P5: owner key file changes require owner sidecar."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import sys
from pathlib import Path

from nouns.owner_sidecar.owner_sidecar import content_hash, verify_sidecar_p1

BASELINE_REL = "integrity/owner-keys/trusted-keys-content-baseline.json"
KEY_FILES = (
    "integrity/owner-keys/TRUSTED_FINGERPRINTS",
    "integrity/owner-keys/richard-pickett.asc",
)


def key_file_change_errors(
    root: Path, *, rel: str, baseline_digest: str, current_digest: str
) -> list[str]:
    """MET when digest unchanged; NOT_MET (non-empty errors) when changed without sidecar."""
    if baseline_digest == current_digest:
        return []
    return verify_sidecar_p1(root, rel)


def key_trust_errors(root: Path) -> list[str]:
    baseline_path = root / BASELINE_REL
    if not baseline_path.is_file():
        return [f"missing {BASELINE_REL}"]
    payload = json.loads(baseline_path.read_text(encoding="utf-8"))
    baseline = payload.get("content_sha256") if isinstance(payload, dict) else None
    if not isinstance(baseline, dict):
        return [f"{BASELINE_REL} must contain content_sha256 object"]
    errors: list[str] = []
    for rel in KEY_FILES:
        file_path = root / rel
        if not file_path.is_file():
            errors.append(f"missing {rel}")
            continue
        digest = content_hash(file_path.read_bytes())
        recorded = baseline.get(rel)
        if not isinstance(recorded, str):
            errors.append(f"{BASELINE_REL} missing entry for {rel}")
            continue
        if digest == recorded:
            continue
        errors.extend(verify_sidecar_p1(root, rel))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = key_trust_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
