"""Hub ./release NOT_MET human surface (ADR 0018 subset — no choice menus)."""

from __future__ import annotations

import sys
from pathlib import Path

BOUNDARY = "bba-emit"

ROOT = Path(__file__).resolve().parents[3]


def merge_main_into_release_remediation(release_branch: str, remote: str = "origin", base: str = "main") -> list[str]:
    return [
        f"git fetch {remote} {base}",
        f"git checkout {release_branch}",
        f"git merge {remote}/{base}",
    ]


def main_purity_remediation(
    *,
    remote: str = "origin",
    base: str = "main",
    next_release_branch: str = "",
    hub: Path | None = None,
) -> list[str]:
    """Copy-paste fixes when main HEAD != last shipped tag (ADR 0044). Fetch alone does not repair purity."""
    hub = (hub or ROOT).resolve()
    sys.path.insert(0, str(hub / "tools"))
    from nouns.release_main_purity import evaluate_main_purity  # noqa: E402

    _ok, _problems, tag, _head = evaluate_main_purity(hub, remote=remote, base=base)
    tag_ref = tag if tag else "v0.0.0"
    work_branch = "ship/next"
    if next_release_branch.startswith("release/v"):
        work_branch = f"work/{next_release_branch.removeprefix('release/v')}"

    return [
        f"git branch {work_branch} HEAD   # preserve unreleased commits (do not ship on {base})",
        f"git fetch {remote} {base} --tags",
        f"git checkout {base}",
        f"git reset --hard {tag_ref}^{{commit}}   # local {base} = last shipped tag",
        f"git checkout {work_branch}",
        f"cd {hub} && ./release",
    ]


def emit_release_not_met(
    problem: str,
    gaps: list[str],
    fix_lines: list[str],
    rerun: str | None = None,
) -> None:
    print("RELEASE:NOT_MET", file=sys.stderr)
    print(f"Problem: {problem}", file=sys.stderr)
    if gaps:
        print("Gaps:", file=sys.stderr)
        for g in gaps:
            print(f"  - {g}", file=sys.stderr)
    if fix_lines:
        print("Fix:", file=sys.stderr)
        for i, line in enumerate(fix_lines, start=1):
            print(f"  {i}. {line}", file=sys.stderr)
    if rerun:
        print(f"Re-run: {rerun}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    _ = argv if argv is not None else sys.argv[1:]
    emit_release_not_met(
        "example",
        ["gap"],
        [f"cd {ROOT} && ./release"],
        f"cd {ROOT} && ./release",
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
