"""Sensitive-file review (ADR 0058). Main's copy of this module grades the branch."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LISTER_REL = "tools/nlc_release_sensitive_review.py"
NOUN_REL = "tools/nouns/sensitive_review/sensitive_review.py"

_ADR = re.compile(r"^adrs/[0-9]{4}-[^/]+\.md$")
_FITNESS = re.compile(r"^tools/fitness-[^/]+\.py$")
_ASSERT = re.compile(r"^tools/assert-[^/]+\.py$")

EXACT: frozenset[str] = frozenset(
    {
        "CHARTER.md",
        "integrity/PRINCIPLES.md",
        "integrity/releasable-gates.json",
        "integrity/known-bad-cases.json",
        "tools/ci_fitness.py",
        "tools/nlc.py",
        "release",
        "scripts/nlc-release.sh",
        LISTER_REL,
        ".github/workflows/fitness.yml",
        ".github/workflows/release.yml",
        ".agents/skills/release/SKILL.md",
        ".agents/skills/planit/SKILL.md",
        ".agents/skills/planit/references/audited-work-loop-standard.md",
    }
)


def norm_rel(rel: str) -> str:
    """Repo-relative posix path."""
    return rel.replace("\\", "/").lstrip("./")


def is_sensitive(rel: str) -> bool:
    """True when rel is on the ADR 0058 prefix table."""
    path = norm_rel(rel)
    if path in EXACT:
        return True
    if _ADR.match(path) or _FITNESS.match(path) or _ASSERT.match(path):
        return True
    return path.startswith("tools/nouns/")


def content_hash(body: bytes) -> str:
    """SHA-256 hex of file bytes."""
    return hashlib.sha256(body).hexdigest()


def sensitive_changes(
    base: dict[str, bytes],
    head: dict[str, bytes],
    *,
    predicate=is_sensitive,
) -> list[tuple[str, str]]:
    """Return (rel, head_hash_or_deleted) for sensitive paths whose bytes differ."""
    names = set(base) | set(head)
    out: list[tuple[str, str]] = []
    for rel in sorted(names):
        if not predicate(rel):
            continue
        old = base.get(rel)
        new = head.get(rel)
        if old == new:
            continue
        if new is None:
            out.append((rel, "deleted"))
        else:
            out.append((rel, content_hash(new)))
    return out


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )


def _blob_at(repo: Path, rev: str, rel: str) -> bytes | None:
    proc = _git(repo, "show", f"{rev}:{rel}")
    if proc.returncode != 0:
        return None
    return proc.stdout.encode("utf-8", errors="surrogateescape")


def _worktree_head(head: str) -> bool:
    """True when head means the working tree, not a git object."""
    return head in {"HEAD", "WORKTREE", ""}


def tree_blobs(repo: Path, rev: str, rels: list[str]) -> dict[str, bytes]:
    """Load blobs at rev for rels that exist. HEAD/WORKTREE reads the working tree."""
    out: dict[str, bytes] = {}
    worktree = _worktree_head(rev)
    for rel in rels:
        if worktree:
            path = repo / rel
            if path.is_file():
                out[rel] = path.read_bytes()
            continue
        body = _blob_at(repo, rev, rel)
        if body is not None:
            out[rel] = body
    return out


def changed_names(repo: Path, base: str, head: str) -> list[str]:
    """git diff names between base and head, including adds and deletes."""
    if _worktree_head(head):
        proc = _git(repo, "diff", "--name-only", base)
        names = [norm_rel(line) for line in (proc.stdout or "").splitlines() if line.strip()]
        extra = _git(repo, "ls-files", "--others", "--exclude-standard")
        names.extend(norm_rel(line) for line in (extra.stdout or "").splitlines() if line.strip())
        return sorted(set(names))
    proc = _git(repo, "diff", "--name-only", f"{base}...{head}")
    names = [norm_rel(line) for line in (proc.stdout or "").splitlines() if line.strip()]
    return sorted(set(names))


def review_errors(repo: Path, base: str, head: str) -> list[str]:
    """NOT_MET lines when a sensitive path differs from base."""
    names = changed_names(repo, base, head)
    base_blobs = tree_blobs(repo, base, names)
    head_blobs = tree_blobs(repo, head, names)
    changes = sensitive_changes(base_blobs, head_blobs)
    return [f"{rel} {digest}" for rel, digest in changes]


def main_has_lister(repo: Path, main_ref: str) -> bool:
    """True when main_ref contains the list-builder."""
    proc = _git(repo, "cat-file", "-e", f"{main_ref}:{LISTER_REL}")
    return proc.returncode == 0


def run_main_copy(repo: Path, main_ref: str, base: str, head: str) -> int:
    """Run origin/main's noun against this tree."""
    with tempfile.TemporaryDirectory(prefix="nlc-sensitive-grader-") as tmp:
        grader = Path(tmp)
        dest = grader / NOUN_REL
        dest.parent.mkdir(parents=True, exist_ok=True)
        proc = _git(repo, "show", f"{main_ref}:{NOUN_REL}")
        if proc.returncode != 0:
            raise SystemExit(f"missing {main_ref}:{NOUN_REL}")
        dest.write_bytes(proc.stdout.encode("utf-8", errors="surrogateescape"))
        ran = subprocess.run(
            [
                sys.executable,
                str(dest),
                "--self",
                "--root",
                str(repo),
                "--base",
                base,
                "--head",
                head,
            ],
            cwd=str(grader),
            check=False,
        )
        return ran.returncode


def emit(errors: list[str]) -> int:
    """Print MET or the unresolved list. Exit 0 only when the list is empty."""
    if errors:
        print("SENSITIVE_REVIEW:NOT_MET")
        for item in errors:
            print(f"PATH {item}")
        print("Fix: revert, edit, or merge the pull request to accept these files.")
        return 1
    print("SENSITIVE_REVIEW:MET")
    return 0


def main() -> int:
    """CLI: grade sensitive-file changes. Default grader is origin/main's copy."""
    parser = argparse.ArgumentParser(description="Sensitive-file review (ADR 0058)")
    parser.add_argument("--check", action="store_true", default=True)
    parser.add_argument("--root", default=None, help="Git repo to grade")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument(
        "--self",
        action="store_true",
        help="Grade with this process's code (used by main's copy and bootstrap)",
    )
    args = parser.parse_args()
    repo = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[3]
    base = args.base
    head = args.head
    if not args.self and main_has_lister(repo, base):
        return run_main_copy(repo, base, base, head)
    return emit(review_errors(repo, base, head))


if __name__ == "__main__":
    raise SystemExit(main())
