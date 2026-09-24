"""Verify hub mirror matches integrity/nlc-install-hashes.json (post-install)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

BOUNDARY = "bba-emit"

HUB_ROOT = Path(__file__).resolve().parents[3]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str] | None = None, hub_root: Path | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    default_hub = (hub_root or HUB_ROOT).resolve()
    hub = Path(args[0]).resolve() if args else default_hub
    manifest = hub / "integrity" / "nlc-install-hashes.json"
    if not manifest.is_file():
        print(
            "Install verification can't run — the hub is missing its fingerprint manifest.",
            file=sys.stderr,
        )
        print(
            "  What's wrong: integrity/nlc-install-hashes.json",
            file=sys.stderr,
        )
        print("  Fix: reinstall from a tagged hub release or a clean git checkout.", file=sys.stderr)
        print("INSTALL_VERIFY:NOT_MET missing integrity/nlc-install-hashes.json", file=sys.stderr)
        return 1
    data = json.loads(manifest.read_text(encoding="utf-8"))
    files: dict[str, str] = dict(data.get("files") or {})
    bad: list[str] = []
    for rel, expected in files.items():
        path = hub / rel
        if not path.is_file():
            bad.append(f"missing {rel}")
            continue
        got = sha256_file(path)
        if got != expected:
            bad.append(f"hash mismatch {rel}")
    if bad:
        print(
            "Install verification failed — hub files don't match the published fingerprints.",
            file=sys.stderr,
        )
        for line in bad[:20]:
            print(f"  What's wrong: {line}", file=sys.stderr)
        if len(bad) > 20:
            print(f"  … and {len(bad) - 20} more", file=sys.stderr)
        print(
            "  Fix: re-run install, or set NLC_SKIP_VERIFY=1 only if you accept an unverified hub.",
            file=sys.stderr,
        )
        print("INSTALL_VERIFY:NOT_MET", file=sys.stderr)
        return 1
    print(f"INSTALL_VERIFY:MET files={len(files)}")
    return 0
