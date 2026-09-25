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
