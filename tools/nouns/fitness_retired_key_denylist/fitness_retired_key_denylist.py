"""C9: RETIRED_FINGERPRINTS denylist; overlap with TRUSTED_FINGERPRINTS is NOT_MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

from nouns.owner_sidecar.owner_sidecar import (
    TRUSTED_REL,
    load_trusted_fingerprints_from_text,
    normalize_fingerprint,
)

ROOT = Path(__file__).resolve().parents[3]
RETIRED_REL = "integrity/owner-keys/RETIRED_FINGERPRINTS"
REQUIRED_RETIRED = "1A86E89505A908766DFD7304F04AD1CEC768DB18"
KNOWN_BAD = ROOT / "tools/fixtures/retired-key/trusted-contains-retired.txt"


def load_retired_fingerprints_from_text(text: str) -> tuple[set[str], list[str]]:
    fps: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fps.add(normalize_fingerprint(line))
    if not fps:
        return set(), ["empty retired fingerprint denylist"]
    return fps, []


def retired_key_errors(
    root: Path, *, trusted_text: str | None = None, retired_text: str | None = None
) -> list[str]:
    errors: list[str] = []
    retired_path = root / RETIRED_REL
    trusted_path = root / TRUSTED_REL
    if retired_text is None:
        if not retired_path.is_file():
            return [f"missing {RETIRED_REL}"]
        retired_text = retired_path.read_text(encoding="utf-8")
    if trusted_text is None:
        if not trusted_path.is_file():
            return [f"missing {TRUSTED_REL}"]
        trusted_text = trusted_path.read_text(encoding="utf-8")
    retired, rerr = load_retired_fingerprints_from_text(retired_text)
    errors.extend(rerr)
    trusted, terr = load_trusted_fingerprints_from_text(trusted_text)
    errors.extend(terr)
    if REQUIRED_RETIRED not in retired:
        errors.append(f"{RETIRED_REL} must contain retired fingerprint {REQUIRED_RETIRED}")
    overlap = sorted(retired & trusted)
    if overlap:
        errors.append(
            "RETIRED_FINGERPRINTS overlap with TRUSTED_FINGERPRINTS: " + ",".join(overlap)
        )
    return errors


def main() -> int:
    errors = retired_key_errors(ROOT)
    if not KNOWN_BAD.is_file():
        errors.append(f"missing known-bad {KNOWN_BAD.relative_to(ROOT)}")
    else:
        retired = (ROOT / RETIRED_REL).read_text(encoding="utf-8") if (ROOT / RETIRED_REL).is_file() else ""
        kb = retired_key_errors(
            ROOT,
            trusted_text=KNOWN_BAD.read_text(encoding="utf-8"),
            retired_text=retired,
        )
        if not any("overlap" in item for item in kb):
            errors.append("known-bad trusted-contains-retired: expected overlap NOT_MET")
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
