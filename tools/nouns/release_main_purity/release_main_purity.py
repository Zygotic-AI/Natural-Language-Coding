"""main HEAD must equal last shipped tag commit (ADR 0044)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from nlc_release_tags import last_shipped_tag, remote_tag_commit  # noqa: E402
from nouns.release_probe.release_probe import (  # noqa: E402
    ProbeFailure,
    confirmed_exists,
    confirmed_text,
    run_argv,
)

BOUNDARY = "bba-emit"

HUB_ROOT = Path(__file__).resolve().parents[3]


def _git(
    *args: str, root: Path, runner: object | None = None
) -> subprocess.CompletedProcess[str]:
    return run_argv(["git", *args], cwd=root, runner=runner)


def resolve_base_head(
    remote: str, base: str, root: Path, runner: object | None = None
) -> str:
    for ref in (f"{remote}/{base}", base, "HEAD"):
        proc = _git("rev-parse", "-q", "--verify", ref, root=root, runner=runner)
        if confirmed_exists(proc, require_stdout=True):
            return (proc.stdout or "").strip()
    raise ProbeFailure("empty output: base head", kind="empty")


def tag_commit(tag: str, root: Path, runner: object | None = None) -> str:
    proc = _git("rev-parse", "-q", "--verify", f"{tag}^{{commit}}", root=root, runner=runner)
    if not confirmed_exists(proc, require_stdout=True):
        return ""
    return (proc.stdout or "").strip()


def commits_after_tag(
    tag: str, head: str, root: Path, runner: object | None = None
) -> list[str]:
    proc = _git("log", f"{tag}..{head}", "--oneline", "-n", "20", root=root, runner=runner)
    confirmed_text(proc, empty_ok=True)
    return [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]


def check_main_purity(
    *,
    head: str,
    tag: str | None,
    tag_at: str,
    tag_known: bool = True,
) -> tuple[bool, list[str]]:
    """Pure when a confirmed empty tag list, or head equals the tag commit.

    Empty or unknown tag peel is NOT_MET (fail-closed). Confirmed no shipped
    tag (tag is None and tag_known) is MET.
    """
    problems: list[str] = []
    if not tag_known:
        problems.append("shipped-tag probe failed or unknown")
        return False, problems
    if not tag:
        return True, problems
    if not tag_at:
        problems.append("empty tag commit (probe failed or unknown)")
        return False, problems
    if not head:
        problems.append("empty HEAD (probe failed or unknown)")
        return False, problems
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
    try:
        head = resolve_base_head(remote, base, hub)
        tag = last_shipped_tag(f"{remote}/{base}", root=hub) or last_shipped_tag(base, root=hub)
        tag_at = remote_tag_commit(tag, remote, hub) if tag else ""
        ok, problems = check_main_purity(head=head, tag=tag, tag_at=tag_at, tag_known=True)
    except ProbeFailure as exc:
        return False, [str(exc)], None, None
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
