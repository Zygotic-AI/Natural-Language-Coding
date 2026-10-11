"""Generate v0.3.0 sync-up review appendix (O4): one R1–R6 theme per changed path."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs" / "reviews" / "v0.3.0-sync-up-file-appendix.md"

DEFAULT_BASE = "5554b8b^"
DEFAULT_HEAD = "5554b8b"
DEFAULT_CHECK_COUNT = 302

THEMES = ("R1", "R2", "R3", "R4", "R5", "R6")


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr or proc.stdout}")
    return proc.stdout


def changed_paths(base: str, head: str) -> list[str]:
    out = git("diff", "--name-only", base, head)
    return sorted(line.strip() for line in out.splitlines() if line.strip())


def diff_stats(base: str, head: str) -> tuple[int, int, int]:
    out = git("diff", "--name-status", base, head)
    added = modified = 0
    for line in out.splitlines():
        if not line.strip():
            continue
        status = line.split("\t", 1)[0]
        if status.startswith("A"):
            added += 1
        elif status.startswith("M"):
            modified += 1
    paths = changed_paths(base, head)
    return len(paths), added, modified


def assign_theme(rel: str) -> str:
    """Exactly one review theme per path (first matching rule wins)."""
    if rel.startswith("adrs/0046-") or rel.startswith("adrs/0047-"):
        return "R1"
    if rel in {
        "integrity/adr-approval-receipts.json",
        "integrity/adr-gates.json",
        "docs/ADR-ENFORCEMENT.md",
    }:
        return "R1"
    if rel.startswith("adrs/0048-"):
        return "R2"
    if rel.startswith("tools/nouns/executable_shape/"):
        return "R2"
    if rel.startswith("goals/"):
        return "R2"
    if rel.startswith("tools/fitness-executable-shape") or rel.endswith(
        "fitness-executable-shape.py"
    ):
        return "R2"
    if rel.startswith("adrs/0049-"):
        return "R3"
    if rel.startswith("tools/nouns/release_state/"):
        return "R3"
    if rel in {"scripts/nlc-release.sh", "docs/adoption/RELEASE.md"}:
        return "R3"
    if rel.startswith("docs/rca/") and "release" in rel.lower():
        return "R3"
    if rel in {"scripts/install.sh", "scripts/install.ps1"}:
        return "R4"
    if rel == "integrity/nlc-install-hashes.json":
        return "R4"
    if rel == ".github/workflows/fitness.yml":
        return "R4"
    if rel.startswith("tools/fitness-hub-x4-tranche") or rel == "integrity/hub-x4-remainder.json":
        return "R5"
    if rel.startswith("tools/nouns/"):
        if rel.startswith("tools/nouns/executable_shape/"):
            return "R2"
        if rel.startswith("tools/nouns/release_state/"):
            return "R3"
        if rel.startswith("tools/nouns/evidence_ref/"):
            return "R6"
        return "R5"
    if rel.startswith("tools/"):
        return "R5"
    if rel in {
        "integrity/hub-content-tree-hash.txt",
        ".nlc/planit-change-evidence.json",
        ".nlc/verified.json",
    }:
        return "R6"
    if "planit-identity" in rel or "no-history-ids-in-evidence" in rel:
        return "R6"
    if rel.startswith("adrs/"):
        return "R1"
    if rel.startswith("integrity/"):
        return "R6"
    if rel.startswith(".nlc/"):
        return "R6"
    if rel.startswith(".cursor/hooks"):
        return "R5"
    if rel.startswith(".agents/"):
        return "R6"
    if rel.startswith("docs/"):
        return "R5"
    if rel.startswith(".github/"):
        return "R4"
    return "R5"


_BASE_RE = re.compile(r"^\*\*Baseline ref:\*\* `([^`]+)`")
_HEAD_RE = re.compile(r"^\*\*Anchor ref:\*\* `([^`]+)`")
_COUNT_RE = re.compile(
    r"^\*\*Path count:\*\* (\d+) \((\d+) added, (\d+) modified"
)
_PATH_RE = re.compile(r"^- `([^`]+)`")


def parse_appendix(text: str) -> tuple[str, str, int, int, int, list[str]]:
    base = head = ""
    total = added = modified = 0
    paths: list[str] = []
    for line in text.splitlines():
        if m := _BASE_RE.match(line.strip()):
            base = m.group(1)
        elif m := _HEAD_RE.match(line.strip()):
            head = m.group(1)
        elif m := _COUNT_RE.match(line.strip()):
            total, added, modified = int(m.group(1)), int(m.group(2)), int(m.group(3))
        elif m := _PATH_RE.match(line.strip()):
            paths.append(m.group(1))
    if not base or not head or not paths:
        raise ValueError("appendix missing baseline, anchor, or path list")
    return base, head, total, added, modified, paths


def render(paths: list[str], base: str, head: str, added: int, modified: int) -> str:
    by_theme: dict[str, list[str]] = {t: [] for t in THEMES}
    for p in paths:
        by_theme[assign_theme(p)].append(p)
    lines = [
        "# v0.3.0 sync-up file appendix (generated)",
        "",
        f"**Baseline ref:** `{base}` (parent of sync-up commit)",
        f"**Anchor ref:** `{head}` (rewrite commit `sync up` on `release/v0.3.0`)",
        f"**Path count:** {len(paths)} ({added} added, {modified} modified in `git diff --name-status`)",
        "",
        "Regenerate: `python3 tools/generate-sync-up-review-appendix.py --check-count 302`",
        "",
    ]
    for theme in THEMES:
        lines.append(f"## {theme} ({len(by_theme[theme])} paths)")
        lines.append("")
        for p in by_theme[theme]:
            lines.append(f"- `{p}`")
        lines.append("")
    return "\n".join(lines)


def verify_committed_appendix() -> int:
    """Fitness entry: committed appendix matches SSOT at default refs."""
    return main_argv(
        [
            "verify",
            "--check-count",
            str(DEFAULT_CHECK_COUNT),
            "--check-only",
        ]
    )


def main_argv(argv: list[str]) -> int:
    old = sys.argv
    sys.argv = argv
    try:
        return main()
    finally:
        sys.argv = old


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        default=DEFAULT_BASE,
        help=f"Git ref for diff base (default: {DEFAULT_BASE})",
    )
    parser.add_argument(
        "--head",
        default=DEFAULT_HEAD,
        help=f"Git ref for sync-up anchor (default: {DEFAULT_HEAD})",
    )
    parser.add_argument(
        "--check-count",
        type=int,
        default=DEFAULT_CHECK_COUNT,
        help=f"Fail unless path count matches (default: {DEFAULT_CHECK_COUNT})",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Verify committed appendix matches generator output; do not write",
    )
    args = parser.parse_args()
    if args.check_only:
        if not OUT.is_file():
            print(f"MISSING {OUT.relative_to(ROOT)}", file=sys.stderr)
            return 1
        committed = OUT.read_text(encoding="utf-8")
        try:
            base, head, total, added, modified, paths = parse_appendix(committed)
        except ValueError as exc:
            print(f"PARSE_FAIL {exc}", file=sys.stderr)
            return 1
        if base != DEFAULT_BASE or head != DEFAULT_HEAD:
            print(
                f"REF_MISMATCH expected {DEFAULT_BASE}..{DEFAULT_HEAD} got {base}..{head}",
                file=sys.stderr,
            )
            return 1
        if args.check_count is not None and len(paths) != args.check_count:
            print(f"COUNT_MISMATCH expected {args.check_count} got {len(paths)}", file=sys.stderr)
            return 1
        if total != len(paths):
            print(f"HEADER_COUNT_MISMATCH header {total} list {len(paths)}", file=sys.stderr)
            return 1
        body = render(sorted(paths), base, head, added, modified)
        if committed != body:
            print(f"DRIFT {OUT.relative_to(ROOT)} (re-run generator)", file=sys.stderr)
            return 1
        print(f"CHECK:MET {OUT.relative_to(ROOT)} ({len(paths)} paths)")
        return 0

    try:
        count, added, modified = diff_stats(args.base, args.head)
        paths = changed_paths(args.base, args.head)
    except RuntimeError as exc:
        print(f"GIT_FAIL {exc}", file=sys.stderr)
        return 1
    if args.check_count is not None and len(paths) != args.check_count:
        print(f"COUNT_MISMATCH expected {args.check_count} got {len(paths)}", file=sys.stderr)
        return 1
    body = render(paths, args.base, args.head, added, modified)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(body, encoding="utf-8")
    print(f"WROTE {OUT.relative_to(ROOT)} ({len(paths)} paths)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
