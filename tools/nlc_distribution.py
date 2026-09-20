"""NLC distribution: semver, store layout, migrations (ADR 0014, 0015)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

DEFAULT_REPO = "Zygotic-AI/Natural-Language-Coding"
DEFAULT_RAW = f"https://raw.githubusercontent.com/{DEFAULT_REPO}/main"
SEMVER_RE = re.compile(r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")

LOCK_SCHEMA = 1


def normalize_version(version: str) -> str:
    m = SEMVER_RE.match(version.strip())
    if not m:
        raise ValueError(f"not semver: {version}")
    return f"{m.group('major')}.{m.group('minor')}.{m.group('patch')}"


def version_key(version: str) -> tuple[int, int, int]:
    a, b, c = normalize_version(version).split(".")
    return int(a), int(b), int(c)


def read_hub_version(hub_root: Path) -> str:
    path = hub_root / "integrity" / "nlc-version.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return normalize_version(str(data["version"]))


def default_install_root() -> Path:
    home = Path.home()
    return home / ".local" / "share" / "nlc"


def versions_dir(install_root: Path) -> Path:
    return install_root / "versions"


def hub_active_path(install_root: Path) -> Path:
    return install_root / "hub"


def current_version_file(install_root: Path) -> Path:
    return install_root / "current"


def read_installed_version(install_root: Path) -> str | None:
    cur = current_version_file(install_root)
    if cur.is_file():
        return normalize_version(cur.read_text(encoding="utf-8").strip())
    hub = hub_active_path(install_root)
    if hub.is_dir() and (hub / "integrity" / "nlc-version.json").is_file():
        return read_hub_version(hub)
    return None


def write_current_version(install_root: Path, version: str) -> None:
    install_root.mkdir(parents=True, exist_ok=True)
    current_version_file(install_root).write_text(
        normalize_version(version) + "\n", encoding="utf-8"
    )


def version_install_path(install_root: Path, version: str) -> Path:
    return versions_dir(install_root) / normalize_version(version)


def link_or_copy_hub(install_root: Path, version: str) -> None:
    src = version_install_path(install_root, version)
    dest = hub_active_path(install_root)
    if not src.is_dir():
        raise FileNotFoundError(f"missing hub version tree: {src}")
    if dest.is_symlink():
        dest.unlink()
    elif dest.is_dir():
        shutil.rmtree(dest)
    elif dest.exists():
        dest.unlink()
    try:
        dest.symlink_to(src.resolve())
    except OSError:
        shutil.copytree(src, dest, symlinks=True, dirs_exist_ok=True)


def published_versions_from_migrations(repo_root: Path) -> list[str]:
    found: set[str] = set()
    mig_root = repo_root / "migrations"
    if not mig_root.is_dir():
        return []
    for child in mig_root.iterdir():
        if not child.is_dir() or "_to_" not in child.name:
            continue
        _, to_part = child.name.split("_to_", 1)
        found.add(normalize_version(to_part))
    ver_file = repo_root / "integrity" / "nlc-version.json"
    if ver_file.is_file():
        found.add(read_hub_version(repo_root))
    return sorted(found, key=version_key)


def migration_dir(repo_root: Path, from_v: str, to_v: str) -> Path:
    a = normalize_version(from_v)
    b = normalize_version(to_v)
    return repo_root / "migrations" / f"{a}_to_{b}"


def semver_upgrade_steps(
    catalog: list[str], from_v: str, to_v: str
) -> list[tuple[str, str]]:
    from_n = normalize_version(from_v)
    to_n = normalize_version(to_v)
    if version_key(from_n) > version_key(to_n):
        raise ValueError(f"downgrade not supported: {from_n} -> {to_n}")
    if from_n == to_n:
        return []
    if not catalog:
        raise ValueError("published version catalog empty")
    if to_n not in catalog:
        raise ValueError(f"target {to_n} not in published catalog")
    if from_n not in catalog:
        raise ValueError(f"installed {from_n} not in published catalog")
    i_from = catalog.index(from_n)
    i_to = catalog.index(to_n)
    if i_from > i_to:
        raise ValueError(f"installed {from_n} newer than target {to_n}")
    steps: list[tuple[str, str]] = []
    for idx in range(i_from + 1, i_to + 1):
        steps.append((catalog[idx - 1], catalog[idx]))
    return steps


def read_migration_kind(mig_dir: Path) -> str:
    yaml_path = mig_dir / "migration.yaml"
    if not yaml_path.is_file():
        raise FileNotFoundError(f"missing {yaml_path}")
    text = yaml_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("kind:"):
            return line.split(":", 1)[1].strip()
    raise ValueError(f"kind not found in {yaml_path}")


def log_upgrade_step(from_v: str, to_v: str, kind: str) -> None:
    print(f"UPGRADE:STEP from={normalize_version(from_v)} to={normalize_version(to_v)} kind={kind}")
    print(f"upgrading to v{normalize_version(to_v)}…")


def log_upgrade_step_completed(to_v: str) -> None:
    print(f"UPGRADE:STEP_COMPLETED to={normalize_version(to_v)}")
    print(f"upgrading to v{normalize_version(to_v)}… completed")


def log_upgrade_met(to_v: str) -> None:
    print(f"UPGRADE:MET to={normalize_version(to_v)}")


def emit_upgrade_not_met(missing: Iterable[str]) -> None:
    print("Upgrade can't continue — something required is missing or invalid.", file=sys.stderr)
    for item in missing:
        print(f"  What's wrong: {item}", file=sys.stderr)
    print("  Fix: run ./nlc doctor fix or reinstall the hub, then ./nlc upgrade", file=sys.stderr)
    print("UPGRADE:NOT_MET", file=sys.stderr)


def run_migration_step(repo_root: Path, from_v: str, to_v: str) -> None:
    mig = migration_dir(repo_root, from_v, to_v)
    if not mig.is_dir():
        emit_upgrade_not_met([f"migration {normalize_version(from_v)}_to_{normalize_version(to_v)}"])
        raise SystemExit(1)
    kind = read_migration_kind(mig)
    log_upgrade_step(from_v, to_v, kind)
    if kind == "noop":
        pass
    elif kind == "script":
        runner = mig / "run"
        if not runner.is_file():
            emit_upgrade_not_met([f"migration script {mig.name}/run"])
            raise SystemExit(1)
        proc = subprocess.run([str(runner)], cwd=mig, check=False)
        if proc.returncode != 0:
            print(f"UPGRADE:STEP_FAILED to={normalize_version(to_v)}", file=sys.stderr)
            raise SystemExit(proc.returncode)
    elif kind == "interview":
        print(
            "UPGRADE:STEP_FAILED to="
            f"{normalize_version(to_v)} (interview gate not automated in v0)",
            file=sys.stderr,
        )
        raise SystemExit(1)
    else:
        emit_upgrade_not_met([f"unknown migration kind {kind!r} in {mig.name}"])
        raise SystemExit(1)
    log_upgrade_step_completed(to_v)


def copy_tree_into_version(src: Path, install_root: Path, version: str) -> Path:
    dest = version_install_path(install_root, version)
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest, symlinks=True, ignore=shutil.ignore_patterns(".git"))
    return dest


def _github_latest_tag(repo: str) -> str | None:
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError:
        return _github_latest_tag_via_ls_remote(repo)
    tag = data.get("tag_name")
    if not tag:
        return None
    return normalize_version(tag)


def github_published_versions(repo: str) -> list[str]:
    if shutil.which("git") is None:
        return []
    proc = subprocess.run(
        ["git", "ls-remote", "--tags", "--refs", f"https://github.com/{repo}.git", "v*"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    tags: list[str] = []
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        ref = parts[1].replace("refs/tags/", "")
        if SEMVER_RE.match(ref):
            tags.append(normalize_version(ref))
    return sorted(set(tags), key=version_key)


def _github_latest_tag_via_ls_remote(repo: str) -> str | None:
    tags = github_published_versions(repo)
    if not tags:
        return None
    return tags[-1]


def resolve_target_version(
    *,
    explicit: str | None,
    install_root: Path,
    repo: str,
) -> str:
    if explicit:
        return normalize_version(explicit)
    latest = _github_latest_tag(repo)
    if latest:
        return latest
    hub = hub_active_path(install_root)
    if hub.is_dir():
        return read_hub_version(hub)
    raise RuntimeError("cannot resolve target version (no release, no hub)")


def download_release_tarball(
    *,
    repo: str,
    version: str,
    dest_file: Path,
) -> None:
    ver = normalize_version(version)
    tag = f"v{ver}"
    names = [f"nlc-{ver}.tar.gz", f"nlc-{tag}.tar.gz"]
    last_err: Exception | None = None
    for name in names:
        url = f"https://github.com/{repo}/releases/download/{tag}/{name}"
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                dest_file.write_bytes(resp.read())
            return
        except Exception as exc:  # noqa: BLE001 — collect for fallback
            last_err = exc
    raise RuntimeError(f"release download failed for {tag}: {last_err}")


def extract_tarball_to_version(tar_path: Path, install_root: Path, version: str) -> Path:
    dest = version_install_path(install_root, version)
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        with tarfile.open(tar_path, "r:gz") as tf:
            tf.extractall(tmp)
        children = [p for p in tmp.iterdir() if p.name != "__MACOSX"]
        if len(children) == 1 and children[0].is_dir():
            shutil.move(str(children[0]), str(dest))
        else:
            dest.mkdir(parents=True, exist_ok=True)
            for child in children:
                shutil.move(str(child), str(dest / child.name))
    return dest


def _git_clone_version(repo: str, version: str, dest: Path) -> None:
    if shutil.which("git") is None:
        raise RuntimeError("git required when release tarball is unavailable")
    tag = f"v{normalize_version(version)}"
    url = f"https://github.com/{repo}.git"
    proc = subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", tag, url, str(dest)],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git clone {tag} failed: {proc.stderr.strip()}")


def fetch_hub_version(
    *,
    install_root: Path,
    version: str,
    repo: str = DEFAULT_REPO,
) -> Path:
    ver = normalize_version(version)
    try:
        with tempfile.TemporaryDirectory() as td:
            tar_path = Path(td) / f"nlc-{ver}.tar.gz"
            download_release_tarball(repo=repo, version=ver, dest_file=tar_path)
            extract_tarball_to_version(tar_path, install_root, ver)
    except RuntimeError:
        with tempfile.TemporaryDirectory() as td:
            clone_dest = Path(td) / "repo"
            _git_clone_version(repo, ver, clone_dest)
            copy_tree_into_version(clone_dest, install_root, ver)
    write_current_version(install_root, ver)
    link_or_copy_hub(install_root, ver)
    return version_install_path(install_root, ver)


def install_hub_from_path(install_root: Path, src_root: Path) -> str:
    ver = read_hub_version(src_root)
    copy_tree_into_version(src_root, install_root, ver)
    write_current_version(install_root, ver)
    link_or_copy_hub(install_root, ver)
    return ver


def write_project_lock(
    project_root: Path,
    *,
    hub_version: str,
    store: str = "user",
    store_path: str | None = None,
) -> Path:
    nlc = project_root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    lock: dict[str, object] = {
        "schema": LOCK_SCHEMA,
        "hub": normalize_version(hub_version),
        "store": store,
    }
    if store_path:
        lock["store_path"] = store_path
    path = nlc / "lock.json"
    path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    return path


def read_project_lock(project_root: Path) -> dict[str, object]:
    path = project_root / ".nlc" / "lock.json"
    if not path.is_file():
        raise FileNotFoundError(f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_install_root_for_lock(project_root: Path, lock: dict[str, object]) -> Path:
    store = str(lock.get("store", "user"))
    if store == "user":
        return default_install_root()
    raw = lock.get("store_path")
    if not raw:
        raise ValueError(f"lock store={store} requires store_path")
    return Path(str(raw)).expanduser().resolve()
