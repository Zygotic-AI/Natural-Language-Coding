#!/usr/bin/env python3
"""Git semver tags for hub release (shipped baseline). Not integrity/nlc-version.json."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def list_version_tags() -> list[str]:
    proc = _git("tag", "-l", "v*.*.*", "--sort=-version:refname")
    if proc.returncode != 0:
        return []
    return [t.strip() for t in (proc.stdout or "").splitlines() if t.strip()]


def tag_exists(tag: str) -> bool:
    proc = _git("rev-parse", "-q", "--verify", f"{tag}^{{commit}}")
    return proc.returncode == 0


def tag_is_ancestor(tag: str, ref: str) -> bool:
    return _git("merge-base", "--is-ancestor", tag, ref).returncode == 0


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


def reachable_tags(to_ref: str = "HEAD") -> list[str]:
    return [t for t in list_version_tags() if tag_exists(t) and tag_is_ancestor(t, to_ref)]


def last_shipped_tag(to_ref: str = "HEAD") -> str | None:
    """Newest v*.*.* tag on history ending at to_ref (what consumers have)."""
    tags = reachable_tags(to_ref)
    return tags[0] if tags else None


def last_shipped_version(to_ref: str = "HEAD") -> str | None:
    tag = last_shipped_tag(to_ref)
    return tag_version(tag) if tag else None


def previous_shipped_tag(before_version: str, to_ref: str = "HEAD") -> str | None:
    """Newest shipped tag strictly before before_version (for changelog since)."""
    tags = reachable_tags(to_ref)
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
