"""Git semver tags for hub release (shipped baseline). Not integrity/nlc-version.json."""

from __future__ import annotations

import subprocess
from pathlib import Path

BOUNDARY = "bba-emit"

HUB_ROOT = Path(__file__).resolve().parents[3]


def _git(*args: str, root: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root or HUB_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def list_version_tags(root: Path | None = None) -> list[str]:
    proc = _git("tag", "-l", "v*.*.*", "--sort=-version:refname", root=root)
    if proc.returncode != 0:
        return []
    return [t.strip() for t in (proc.stdout or "").splitlines() if t.strip()]


def tag_exists(tag: str, root: Path | None = None) -> bool:
    proc = _git("rev-parse", "-q", "--verify", f"{tag}^{{commit}}", root=root)
    return proc.returncode == 0


def tag_commit(tag: str, root: Path | None = None) -> str:
    proc = _git("rev-parse", f"{tag}^{{commit}}", root=root)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def remote_tag_commit_only(tag: str, remote: str = "origin", root: Path | None = None) -> str:
    """Peeled commit for refs/tags/{tag} on remote (annotated tag object id is not the commit)."""
    peeled = _git("ls-remote", remote, f"refs/tags/{tag}^{{}}", root=root)
    if peeled.returncode == 0 and peeled.stdout.strip():
        parts = peeled.stdout.strip().splitlines()[0].split()
        if parts:
            return parts[0]
    proc = _git("ls-remote", remote, f"refs/tags/{tag}", root=root)
    if proc.returncode == 0 and proc.stdout.strip():
        parts = proc.stdout.strip().splitlines()[0].split()
        if parts:
            return parts[0]
    return ""


def remote_tag_commit(tag: str, remote: str = "origin", root: Path | None = None) -> str:
    """Remote shipped tag commit when resolvable, else local peeled tag."""
    remote_at = remote_tag_commit_only(tag, remote, root)
    if remote_at:
        return remote_at
    return tag_commit(tag, root)


def canonical_tag_commit(tag: str, remote: str = "origin", root: Path | None = None) -> str:
    """SSOT shipped baseline commit for reset/verify (prefer remote tag object)."""
    return remote_tag_commit(tag, remote, root)


def local_remote_tag_divergence(
    tag: str, remote: str = "origin", root: Path | None = None
) -> tuple[str, str] | None:
    """(local_commit, remote_commit) when both exist and differ."""
    local = tag_commit(tag, root)
    remote_at = remote_tag_commit_only(tag, remote, root)
    if local and remote_at and local != remote_at:
        return local, remote_at
    return None


def align_local_tag_to_remote(
    tag: str, remote: str = "origin", root: Path | None = None
) -> str | None:
    """Replace local tag with the remote tag ref. Does not push. Returns peeled commit or None."""
    diverged = local_remote_tag_divergence(tag, remote, root)
    if not diverged:
        return None
    proc = _git("fetch", remote, f"+refs/tags/{tag}:refs/tags/{tag}", root=root)
    if proc.returncode != 0:
        return None
    return tag_commit(tag, root) or None


def tag_is_ancestor(tag: str, ref: str, root: Path | None = None) -> bool:
    return _git("merge-base", "--is-ancestor", tag, ref, root=root).returncode == 0


def tag_key(tag: str) -> tuple[int, int, int]:
    body = tag.lstrip("v")
    parts = body.split(".")
    if len(parts) != 3:
        return (0, 0, 0)
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return (0, 0, 0)


def tag_version(tag: str) -> str:
    return tag.lstrip("v")


def reachable_tags(to_ref: str = "HEAD", root: Path | None = None) -> list[str]:
    return [
        t
        for t in list_version_tags(root)
        if tag_exists(t, root) and tag_is_ancestor(t, to_ref, root)
    ]


def last_shipped_tag(to_ref: str = "HEAD", root: Path | None = None) -> str | None:
    tags = reachable_tags(to_ref, root)
    return tags[0] if tags else None


def last_shipped_version(to_ref: str = "HEAD", root: Path | None = None) -> str | None:
    tag = last_shipped_tag(to_ref, root)
    return tag_version(tag) if tag else None


def resolve_shipped_baseline(
    to_ref: str = "HEAD", root: Path | None = None
) -> tuple[str | None, str | None]:
    """Newest reachable tag on ref, else highest semver tag name (rewritten main)."""
    shipped_tag = last_shipped_tag(to_ref, root)
    if shipped_tag:
        return shipped_tag, tag_version(shipped_tag)
    tags = list_version_tags(root)
    if not tags:
        return None, None
    fallback = tags[0]
    if tag_is_ancestor(fallback, to_ref, root):
        return fallback, tag_version(fallback)
    return fallback, tag_version(fallback)


def resolve_shipped_version(to_ref: str = "HEAD", root: Path | None = None) -> str | None:
    _tag, ver = resolve_shipped_baseline(to_ref, root)
    return ver


def previous_shipped_tag(
    before_version: str, to_ref: str = "HEAD", root: Path | None = None
) -> str | None:
    tags = reachable_tags(to_ref, root)
    if not tags:
        return None
    target = f"v{before_version.lstrip('v')}"
    for tag in tags:
        if tag == target:
            continue
        if tag_key(tag) < tag_key(target):
            return tag
    return None


def parse_semver(version: str) -> tuple[int, int, int]:
    parts = version.lstrip("v").split(".")
    return (int(parts[0]), int(parts[1]), int(parts[2]))
