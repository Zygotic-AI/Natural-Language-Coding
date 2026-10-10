#!/usr/bin/env python3
"""ADR 0040: last shipped tag must pass release tag gate (static); print remediation."""

from __future__ import annotations

BOUNDARY = "bba-emit"


import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_release_tag_gate import check_static, tag_from_version  # noqa: E402
from nlc_release_tags import (  # noqa: E402
    align_local_tag_to_remote,
    canonical_tag_commit,
    last_shipped_tag,
    local_remote_tag_divergence,
    tag_version,
)
from nlc_requirements import hub_tool  # noqa: E402
from nouns.evidence_ref.evidence_ref import refuse_gate, resolve_commit  # noqa: E402


def _git_rev_parse(repo_root: Path, ref: str) -> str | None:
    proc = subprocess.run(
        ["git", "rev-parse", ref],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return (proc.stdout or "").strip()


def remediation_lines(tag: str) -> list[str]:
    return [
        "  Fix options (choose explicitly; ADR 0040):",
        f"    A) Remove mistaken tag: git tag -d {tag} && git push origin :refs/tags/{tag}",
        "    B) Ship a valid release from ./release (record + notes + verify-deep), then retag:",
        f"       NLC_RELEASE_ALLOW_RETAG=1 ./release",
        "  Policy: docs/adoption/RELEASE.md — do not use ./release finish alone.",
    ]


def audit_tag_commit(tag: str, commit: str, *, repo_root: Path) -> tuple[bool, list[str]]:
    ver = tag_version(tag)
    problems = check_static(repo_root, commit, tag)
    if problems:
        return False, problems
    if tag_from_version(ver) != tag:
        return False, [f"tag {tag} name mismatch"]
    return True, []


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Audit last shipped tag against tag gate (static)")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--to", dest="to_ref", default="HEAD", help="Git ref for tag ancestry")
    parser.add_argument("--tag", default=None, help="Override tag (landmine / tests)")
    parser.add_argument("--commit", default=None, help="Override commit (with --tag)")
    parser.add_argument("--remote", default="origin")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Git root for --tag/--commit landmine overrides (default hub checkout)",
    )
    parser.add_argument(
        "--align-local",
        action="store_true",
        help="Move local shipped tag to origin commit before audit (no push)",
    )
    args = parser.parse_args()

    if not args.check:
        parser.print_help()
        return 2

    repo_root = Path(args.repo_root).resolve() if args.repo_root else ROOT

    if args.tag and args.commit:
        tag = args.tag.strip()
        commit = args.commit.strip()
        _, err = resolve_commit(repo_root, commit)
        if err:
            return refuse_gate("RELEASE_SHIPPED_TAG", commit, err)
    else:
        tag = last_shipped_tag(args.to_ref)
        if not tag:
            print("RELEASE_SHIPPED_TAG:MET (no v*.*.* tag on history)")
            return 0
        if args.align_local:
            moved = align_local_tag_to_remote(tag, args.remote, ROOT)
            if moved:
                print(
                    f"RELEASE_SHIPPED_TAG:ALIGNED {tag} -> {moved[:12]} "
                    f"(local only; matches {args.remote}; no push)"
                )
        diverged = local_remote_tag_divergence(tag, args.remote, ROOT)
        if diverged:
            local_at, remote_at = diverged
            print("RELEASE_SHIPPED_TAG:NOT_MET", file=sys.stderr)
            print(
                f"  What's wrong: local {tag} at {local_at[:12]} != "
                f"{args.remote} tag at {remote_at[:12]}",
                file=sys.stderr,
            )
            print(
                f"  fix: git fetch {args.remote} --tags && git tag -f {tag} {remote_at} "
                f"(or delete local tag and re-fetch)",
                file=sys.stderr,
            )
            return 1
        commit = canonical_tag_commit(tag, args.remote, ROOT)
        if not commit:
            commit = _git_rev_parse(ROOT, f"{tag}^{{commit}}")
        if not commit:
            print("RELEASE_SHIPPED_TAG:NOT_MET", file=sys.stderr)
            print(f"  What's wrong: cannot resolve commit for tag {tag}", file=sys.stderr)
            return 1
        repo_root = ROOT

    ok, problems = audit_tag_commit(tag, commit, repo_root=repo_root)
    if ok:
        print(f"RELEASE_SHIPPED_TAG:MET tag={tag} commit={commit[:12]}")
        return 0

    print("RELEASE_SHIPPED_TAG:NOT_MET", file=sys.stderr)
    print(f"  What's wrong: tag {tag} at {commit[:12]} fails release tag gate", file=sys.stderr)
    print("  Why it blocks: ADR 0039 — tags must prove ./release ritual on that commit", file=sys.stderr)
    for p in problems:
        print(f"  - {p}", file=sys.stderr)
    for line in remediation_lines(tag):
        print(line, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
