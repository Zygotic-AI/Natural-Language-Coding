"""Fetch or register a hub version into the user store (ADR 0015)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from nlc_distribution import (
    DEFAULT_REPO,
    default_install_root,
    fetch_hub_version,
    install_hub_from_path,
    read_installed_version,
    resolve_target_version,
)

BOUNDARY = "bba-emit"


def main(argv: list[str] | None = None) -> int:
    args_list = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description="Install NLC hub into version store")
    parser.add_argument(
        "--install-root",
        type=Path,
        default=None,
        help="Store root (default ~/.local/share/nlc)",
    )
    parser.add_argument("--version", default=None, help="Semver hub version to fetch")
    parser.add_argument(
        "--from-path",
        type=Path,
        default=None,
        help="Copy hub tree from local checkout instead of release tarball",
    )
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repo slug")
    args = parser.parse_args(args_list)

    install_root = (args.install_root or default_install_root()).expanduser().resolve()
    install_root.mkdir(parents=True, exist_ok=True)

    if args.from_path:
        src = args.from_path.resolve()
        ver = install_hub_from_path(install_root, src)
        print(f"INSTALL:MET hub={ver} store={install_root}")
        return 0

    target = resolve_target_version(
        explicit=args.version,
        install_root=install_root,
        repo=args.repo,
    )
    installed = read_installed_version(install_root)
    if installed == target and (install_root / "hub").exists():
        print(f"INSTALL:MET hub={target} store={install_root} (already current)")
        return 0

    fetch_hub_version(install_root=install_root, version=target, repo=args.repo)
    print(f"INSTALL:MET hub={target} store={install_root}")
    return 0
