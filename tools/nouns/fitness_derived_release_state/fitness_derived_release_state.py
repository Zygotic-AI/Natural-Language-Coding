"""One suite check for derived release files (ADR 0057). No owner armor."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

from nouns.checker_digest.checker_digest import digest_errors
from nouns.gate_set_manifest.gate_set_manifest import gate_set_manifest_errors
from nouns.install_hash_update.install_hash_update import collect_install_files
from nouns.mandated_paths.mandated_paths import snapshot_errors as mandated_errors
from nouns.self_ref_set.self_ref_set import snapshot_errors as self_ref_errors

INSTALL_REL = "integrity/nlc-install-hashes.json"


def install_hash_errors(root: Path) -> list[str]:
    files = collect_install_files(root)
    path = root / INSTALL_REL
    if files is None:
        return [f"{INSTALL_REL}: required install path missing"]
    if not path.is_file():
        return [f"missing {INSTALL_REL}"]
    try:
        on_disk = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{INSTALL_REL}: JSON error {exc}"]
    if not isinstance(on_disk, dict) or on_disk.get("files") != files:
        return [f"{INSTALL_REL}: drift versus install hash inputs (regenerate)"]
    return []


def derived_release_state_errors(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(digest_errors(root))
    errors.extend(gate_set_manifest_errors(root))
    errors.extend(mandated_errors(root))
    errors.extend(self_ref_errors(root))
    errors.extend(install_hash_errors(root))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = derived_release_state_errors(root)
    if errors:
        print(f"VIOLATION {errors[0]}")
        if len(errors) > 1:
            print(f"VIOLATION {len(errors) - 1} more derived-release-state drift(s)")
        print("RESULT:NOT_MET")
        print("Reproduce: python3 tools/regen-derived-release-state.py")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
