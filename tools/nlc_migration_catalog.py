"""ADR 0014: hub semver catalog must match migration units."""

from __future__ import annotations

from pathlib import Path

from nlc_distribution import (
    migration_dir,
    normalize_version,
    published_versions_from_migrations,
    read_hub_version,
    semver_upgrade_steps,
    version_key,
)


def migration_catalog_blockers(repo_root: Path) -> list[str]:
    catalog = published_versions_from_migrations(repo_root)
    hub = read_hub_version(repo_root)
    blockers: list[str] = []
    if not catalog:
        blockers.append("migration catalog empty (migrations/ + nlc-version.json)")
        return blockers
    if hub not in catalog:
        blockers.append(f"hub version {hub} not in migration catalog")
    try:
        steps = semver_upgrade_steps(catalog, catalog[0], hub)
    except ValueError as exc:
        blockers.append(str(exc))
        return blockers
    for from_v, to_v in steps:
        mig = migration_dir(repo_root, from_v, to_v)
        if not mig.is_dir():
            blockers.append(f"missing migration {mig.name}")
            continue
        if not (mig / "migration.yaml").is_file():
            blockers.append(f"missing {mig.name}/migration.yaml")
    return blockers


def planning_catalog(repo_root: Path, target: str) -> list[str]:
    """Versions needed to compute upgrade steps toward target (before version file bump)."""
    catalog = set(published_versions_from_migrations(repo_root))
    catalog.add(normalize_version(read_hub_version(repo_root)))
    catalog.add(normalize_version(target))
    return sorted(catalog, key=version_key)


def upgrade_steps_toward(repo_root: Path, from_v: str, to_v: str) -> list[tuple[str, str]]:
    from_n = normalize_version(from_v)
    to_n = normalize_version(to_v)
    if from_n == to_n:
        return []
    catalog = planning_catalog(repo_root, to_n)
    return semver_upgrade_steps(catalog, from_n, to_n)


def write_noop_migration_unit(repo_root: Path, from_v: str, to_v: str) -> Path:
    mig_root = migration_dir(repo_root, from_v, to_v)
    if not mig_root.is_dir():
        mig_root.mkdir(parents=True, exist_ok=True)
    yaml_path = mig_root / "migration.yaml"
    if not yaml_path.is_file():
        yaml_path.write_text(
            f"from: {normalize_version(from_v)}\n"
            f"to: {normalize_version(to_v)}\n"
            "kind: noop\n",
            encoding="utf-8",
        )
    return mig_root


def ensure_migration_chain(repo_root: Path, from_v: str, to_v: str) -> list[Path]:
    created: list[Path] = []
    for a, b in upgrade_steps_toward(repo_root, from_v, to_v):
        mig = migration_dir(repo_root, a, b)
        if not mig.is_dir() or not (mig / "migration.yaml").is_file():
            created.append(write_noop_migration_unit(repo_root, a, b))
    return created


def release_target_blockers(
    repo_root: Path, target: str, shipped_from: str
) -> list[str]:
    """Gates for publishing target from last shipped semver (ADR 0014, ADR 0022)."""
    target_n = normalize_version(target)
    shipped_n = normalize_version(shipped_from)
    blockers: list[str] = []
    if version_key(target_n) < version_key(shipped_n):
        blockers.append(f"target {target_n} is behind shipped {shipped_n}")
        return blockers
    if target_n == shipped_n:
        return blockers
    return migration_steps_blockers(repo_root, shipped_n, target_n)


def migration_steps_blockers(repo_root: Path, from_v: str, to_v: str) -> list[str]:
    blockers: list[str] = []
    try:
        steps = upgrade_steps_toward(repo_root, from_v, to_v)
    except ValueError as exc:
        return [str(exc)]
    for a, b in steps:
        mig = migration_dir(repo_root, a, b)
        if not mig.is_dir():
            blockers.append(f"missing migration {mig.name}")
        elif not (mig / "migration.yaml").is_file():
            blockers.append(f"missing {mig.name}/migration.yaml")
    return blockers
