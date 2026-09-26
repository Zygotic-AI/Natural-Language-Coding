"""main HEAD must equal last shipped tag commit (ADR 0044)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from nlc_release_tags import last_shipped_tag, remote_tag_commit  # noqa: E402

BOUNDARY = "bba-emit"

HUB_ROOT = Path(__file__).resolve().parents[3]


def _git(*args: str, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )


def resolve_base_head(remote: str, base: str, root: Path) -> str:
    for ref in (f"{remote}/{base}", base):
        proc = _git("rev-parse", ref, root=root)
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    proc = _git("rev-parse", "HEAD", root=root)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def tag_commit(tag: str, root: Path) -> str:
    proc = _git("rev-parse", f"{tag}^{{commit}}", root=root)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def commits_after_tag(tag: str, head: str, root: Path) -> list[str]:
    proc = _git("log", f"{tag}..{head}", "--oneline", "-n", "20", root=root)
    if proc.returncode != 0:
        return []
    return [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]


def check_main_purity(
    *,
    head: str,
    tag: str | None,
    tag_at: str,
) -> tuple[bool, list[str]]:
    """Pure when no tag yet, or head equals tag commit."""
    problems: list[str] = []
    if not tag or not tag_at:
        return True, problems
    if head == tag_at:
        return True, problems
    problems.append(f"main ({head[:12]}) is not at last shipped tag {tag} ({tag_at[:12]})")
    return False, problems


def evaluate_main_purity(
    hub: Path,
    remote: str = "origin",
    base: str = "main",
    to_ref: str | None = None,
) -> tuple[bool, list[str], str | None, str | None]:
    head = resolve_base_head(remote, base, hub)
    tag = last_shipped_tag(f"{remote}/{base}", root=hub) or last_shipped_tag(base, root=hub)
    tag_at = remote_tag_commit(tag, remote, hub) if tag else ""
    ok, problems = check_main_purity(head=head, tag=tag, tag_at=tag_at)
    if not ok and tag:
        for ln in commits_after_tag(tag, head, hub):
            problems.append(f"  commit on main after tag: {ln}")
    return ok, problems, tag, head


def main(argv: list[str] | None = None, hub_root: Path | None = None) -> int:
    import argparse

    hub = (hub_root or HUB_ROOT).resolve()
    args_list = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description="main production-trunk purity (ADR 0044)")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    args = parser.parse_args(args_list)

    if not args.check:
        parser.print_help()
        return 2

    ok, problems, tag, head = evaluate_main_purity(hub, remote=args.remote, base=args.base)
    print(f"RELEASE_MAIN_PURITY: tag={tag or 'none'} head={head[:12] if head else 'none'}")
    if ok:
        print("RELEASE_MAIN_PURITY:MET")
        return 0
    print("RELEASE_MAIN_PURITY:NOT_MET", file=sys.stderr)
    for line in problems:
        print(f"  {line}", file=sys.stderr)
    if tag:
        canon = remote_tag_commit(tag, args.remote, hub)
        print(
            f"  fix: git fetch {args.remote} --tags && git checkout {args.base} && git reset --hard {canon or tag}",
            file=sys.stderr,
        )
        print(
            "  fix: move unreleased work to release/v* before reset (branch from main, cherry-pick)",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    sys.exit(main())
