"""Generate v0.3.0 sync-up review appendix (O4): one R1–R6 theme per changed path."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs" / "reviews" / "v0.3.0-sync-up-file-appendix.md"

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


def render(paths: list[str], base: str, head: str) -> str:
    by_theme: dict[str, list[str]] = {t: [] for t in THEMES}
    for p in paths:
        by_theme[assign_theme(p)].append(p)
    lines = [
        "# v0.3.0 sync-up file appendix (generated)",
        "",
        f"**Baseline ref:** `{base}`",
        f"**Anchor ref:** `{head}` (`release/v0.3.0` batch-1 stabilization)",
        f"**Path count:** {len(paths)} (enumerator SSOT; historical “302-file bundle” label predates this anchor)",
        "",
        "Regenerate: `python3 tools/generate-sync-up-review-appendix.py`",
        "",
    ]
    for theme in THEMES:
        lines.append(f"## {theme} ({len(by_theme[theme])} paths)")
        lines.append("")
        for p in by_theme[theme]:
            lines.append(f"- `{p}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        default=None,
        help="Git ref for diff base (default: merge-base origin/main origin/release/v0.3.0)",
    )
    parser.add_argument(
        "--head",
        default="4120ff4",
        help="Git ref for sync-up anchor (default: 4120ff4 on release/v0.3.0)",
    )
    parser.add_argument("--check-count", type=int, default=None, help="Fail unless path count matches")
    args = parser.parse_args()
    base = args.base
    if not base:
        base = git("merge-base", "origin/main", "origin/release/v0.3.0").strip()
    paths = changed_paths(base, args.head)
    if args.check_count is not None and len(paths) != args.check_count:
        print(f"COUNT_MISMATCH expected {args.check_count} got {len(paths)}", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(paths, base, args.head), encoding="utf-8")
    print(f"WROTE {OUT.relative_to(ROOT)} ({len(paths)} paths)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
