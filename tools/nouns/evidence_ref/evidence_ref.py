"""Content-addressed evidence identity (ADR 0050): tree/blob hashes, not commit ids."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BOUNDARY = "bba-emit"

COMMIT_HEX = re.compile(r"\b[0-9a-f]{7,40}\b", re.I)
SHA256_HEX = re.compile(r"\b[0-9a-f]{64}\b", re.I)


def git_run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run git in root with captured stdout/stderr."""
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )


def object_type(root: Path, ref: str) -> str | None:
    """Return git object type for ref, or None if unresolvable."""
    proc = git_run(root, "cat-file", "-t", ref)
    if proc.returncode != 0:
        return None
    return (proc.stdout or "").strip()


def is_resolvable_commit(root: Path, ref: str) -> bool:
    """True when ref resolves to a commit object in root's repository."""
    proc = git_run(root, "rev-parse", "--verify", f"{ref}^{{commit}}")
    return proc.returncode == 0


def resolve_commit(root: Path, ref: str) -> tuple[str | None, str | None]:
    """
    Resolve ref to a full commit sha.

    Returns (sha, None) on success or (None, error_message) when unresolvable.
    """
    ref = ref.strip()
    if not ref:
        return None, "empty reference"
    proc = git_run(root, "rev-parse", "--verify", f"{ref}^{{commit}}")
    if proc.returncode != 0:
        return None, f"unresolved commit reference: {ref}"
    return (proc.stdout or "").strip(), None


def tree_hash_at_commit(root: Path, commit: str) -> tuple[str | None, str | None]:
    """Return the git tree hash at commit, or (None, error) when unresolvable."""
    sha, err = resolve_commit(root, commit)
    if err:
        return None, err
    proc = git_run(root, "rev-parse", f"{sha}^{{tree}}")
    if proc.returncode != 0:
        return None, f"cannot read tree at commit {commit}"
    return (proc.stdout or "").strip(), None


def worktree_tree_hash_excluding(root: Path, exclude_rel: set[str]) -> str:
    """
    Git tree hash for staged worktree changes while excluded paths stay at HEAD index entries.

    Used for self-describing hub-content-tree-hash.txt (ADR 0050).
    """
    fd, raw = tempfile.mkstemp(prefix="nlc-evidence-index-")
    os.close(fd)
    index_path = Path(raw)
    index_path.unlink(missing_ok=True)
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = raw
    try:
        read = git_run(root, "read-tree", "HEAD")
        if read.returncode != 0:
            return ""
        add = subprocess.run(
            ["git", "add", "-A"],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if add.returncode != 0:
            return ""
        for rel in sorted(exclude_rel):
            subprocess.run(
                ["git", "reset", "HEAD", "--", rel],
                cwd=str(root),
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
        tree = subprocess.run(
            ["git", "write-tree"],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        return tree.stdout.strip() if tree.returncode == 0 else ""
    finally:
        index_path.unlink(missing_ok=True)


def worktree_tree_hash(root: Path) -> str:
    """
    Hash tracked and untracked worktree content (same model as release effective_tree_sha).

    Returns empty string when git cannot build the tree.
    """
    fd, raw = tempfile.mkstemp(prefix="nlc-evidence-index-")
    os.close(fd)
    index_path = Path(raw)
    index_path.unlink(missing_ok=True)
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = raw
    try:
        read = git_run(root, "read-tree", "HEAD")
        if read.returncode != 0:
            return ""
        add = subprocess.run(
            ["git", "add", "-A"],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if add.returncode != 0:
            return ""
        tree = subprocess.run(
            ["git", "write-tree"],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        return tree.stdout.strip() if tree.returncode == 0 else ""
    finally:
        index_path.unlink(missing_ok=True)


def head_tree_hash(root: Path) -> str:
    """Return HEAD^{tree} or empty string."""
    proc = git_run(root, "rev-parse", "HEAD^{tree}")
    return (proc.stdout or "").strip() if proc.returncode == 0 else ""


def hub_version(root: Path) -> str:
    """Read integrity/nlc-version.json version field."""
    path = root / "integrity" / "nlc-version.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(payload.get("version") or "").strip()


def refuse_gate(prefix: str, reference: str, detail: str = "") -> int:
    """Print REFUSE outcome for a gate prefix (e.g. RELEASE_TAG_GATE)."""
    print(f"{prefix}:REFUSE", file=sys.stderr)
    print(f"  Unresolved reference: {reference}", file=sys.stderr)
    if detail:
        print(f"  {detail}", file=sys.stderr)
    return 2


def iter_commit_hex_tokens(text: str) -> list[str]:
    """Find 7–40 hex tokens that are not substrings of sha256 digests."""
    without_sha256 = SHA256_HEX.sub("", text)
    return COMMIT_HEX.findall(without_sha256)


def commit_pins_in_text(root: Path, text: str) -> list[str]:
    """Return commit refs in text that resolve in root's git object database."""
    pins: list[str] = []
    seen: set[str] = set()
    for token in iter_commit_hex_tokens(text):
        key = token.lower()
        if key in seen:
            continue
        seen.add(key)
        if is_resolvable_commit(root, token):
            pins.append(token)
    return pins


def init_bare_repo(repo: Path) -> None:
    """Initialize an empty git repository with deterministic user identity."""
    subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "evidence-ref@example.com"],
        cwd=str(repo),
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "evidence-ref"],
        cwd=str(repo),
        check=True,
        capture_output=True,
    )


def commit_all(repo: Path, message: str) -> str:
    """Stage all files and create a commit; return full commit sha."""
    subprocess.run(["git", "add", "-A"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=str(repo),
        check=True,
        capture_output=True,
    )
    proc = git_run(repo, "rev-parse", "HEAD")
    return (proc.stdout or "").strip()
