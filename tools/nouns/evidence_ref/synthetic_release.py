"""Synthetic git repos for release landmines (ADR 0050 self-contained fixtures)."""

from __future__ import annotations

import json
from pathlib import Path

from nouns.evidence_ref.evidence_ref import commit_all, init_bare_repo


def unprepared_release_commit(repo: Path, version: str = "0.2.0") -> str:
    """
    Create a commit with version file and release notes but no hub-release-record.json.

    Returns the full commit sha.
    """
    init_bare_repo(repo)
    integrity = repo / "integrity"
    integrity.mkdir(parents=True)
    (integrity / "nlc-version.json").write_text(
        json.dumps({"version": version}, indent=2) + "\n",
        encoding="utf-8",
    )
    docs = repo / "docs" / "adoption"
    docs.mkdir(parents=True)
    (docs / f"RELEASE-v{version}.md").write_text(
        f"# Release v{version}\n\n## Highlights\n\n- synthetic landmine specimen\n",
        encoding="utf-8",
    )
    return commit_all(repo, f"synthetic unprepared release v{version}")
