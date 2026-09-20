#!/usr/bin/env python3
"""Upgrade hub semver chain with explicit migrations (ADR 0014)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_distribution import (  # noqa: E402
    DEFAULT_REPO,
    emit_upgrade_not_met,
    fetch_hub_version,
    github_published_versions,
    hub_active_path,
    log_upgrade_met,
    published_versions_from_migrations,
    read_installed_version,
    read_project_lock,
    resolve_install_root_for_lock,
    resolve_target_version,
    run_migration_step,
    semver_upgrade_steps,
    write_project_lock,
)
from nlc_requirements import hub_tool  # noqa: E402


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Upgrade NLC hub in store and project lock")
    parser.add_argument(
        "--project",
        type=Path,
        default=Path.cwd(),
        help="Compiled-system repo with .nlc/lock.json",
    )
    parser.add_argument("--to", dest="to_version", default=None, help="Target semver (default latest)")
    parser.add_argument("--install-root", type=Path, default=None, help="Override store root")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repo slug")
    args = parser.parse_args()

    project = args.project.resolve()
    try:
        lock = read_project_lock(project)
    except FileNotFoundError:
        print("UPGRADE:NOT_MET", file=sys.stderr)
        print("  missing: .nlc/lock.json (run nlc-init or create lock)", file=sys.stderr)
        return 1

    install_root = (
        args.install_root.expanduser().resolve()
        if args.install_root
        else resolve_install_root_for_lock(project, lock)
    )
    hub = hub_active_path(install_root)
    if not hub.is_dir():
        print("UPGRADE:NOT_MET", file=sys.stderr)
        print(f"  missing: hub at {hub}", file=sys.stderr)
        return 1

    repo_root = hub.resolve()
    from_v = str(lock.get("hub", ""))
    if not from_v:
        emit_upgrade_not_met(["lock field hub"])
        return 1

    try:
        target = resolve_target_version(
            explicit=args.to_version,
            install_root=install_root,
            repo=args.repo,
        )
    except RuntimeError as exc:
        print("UPGRADE:NOT_MET", file=sys.stderr)
        print(f"  missing: {exc}", file=sys.stderr)
        return 1

    catalog = github_published_versions(args.repo)
    if not catalog:
        catalog = published_versions_from_migrations(repo_root)
    try:
        steps = semver_upgrade_steps(catalog, from_v, target)
    except ValueError as exc:
        print("UPGRADE:NOT_MET", file=sys.stderr)
        print(f"  missing: {exc}", file=sys.stderr)
        return 1

    for step_from, step_to in steps:
        fetch_hub_version(install_root=install_root, version=step_to, repo=args.repo)
        new_root = hub_active_path(install_root).resolve()
        run_migration_step(new_root, step_from, step_to)

    if from_v != target or steps:
        store = str(lock.get("store", "user"))
        store_path = lock.get("store_path")
        write_project_lock(
            project,
            hub_version=target,
            store=store,
            store_path=str(store_path) if store_path else None,
        )

    installed = read_installed_version(install_root)
    if installed:
        log_upgrade_met(installed)
    else:
        log_upgrade_met(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
