"""Hub release notes: draft from last tag, validate Highlights, refresh change log."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import re
import subprocess
import sys
from pathlib import Path

from nlc_release_tags import previous_shipped_tag, tag_exists

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402
NOTES_DIR = ROOT / "docs" / "adoption"
HIGHLIGHTS_PLACEHOLDER = "Replace this block with user-facing summary (required)."


def notes_path(version: str) -> Path:
    ver = version.lstrip("v")
    return NOTES_DIR / f"RELEASE-v{ver}.md"


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def changelog_base_tag(release_version: str, to_ref: str) -> str | None:
    """Git tag to start changelog from — never integrity/nlc-version.json."""
    return previous_shipped_tag(release_version, to_ref)


def commit_lines(from_ref: str, to_ref: str) -> list[str]:
    proc = _git(
        "log",
        f"{from_ref}..{to_ref}",
        "--pretty=format:- %s (`%h`)",
        "--no-merges",
    )
    if proc.returncode != 0:
        return []
    lines = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]
    if lines:
        return lines
    proc = _git(
        "log",
        f"{from_ref}..{to_ref}",
        "--pretty=format:- %s (`%h`)",
    )
    return [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]


def diff_stat(from_ref: str, to_ref: str) -> str:
    proc = _git("diff", "--stat", f"{from_ref}..{to_ref}")
    if proc.returncode != 0 or not (proc.stdout or "").strip():
        return ""
    return proc.stdout.strip()


def build_draft(version: str, to_ref: str, from_tag: str | None) -> str:
    ver = version.lstrip("v")
    if from_tag:
        commits = commit_lines(from_tag, to_ref)
        heading = f"## Changes since {from_tag}"
        stat = diff_stat(from_tag, to_ref)
    else:
        proc = _git("log", to_ref, "--pretty=format:- %s (`%h`)", "-n", "50")
        commits = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]
        heading = "## Changes (no prior semver tag in repo)"
        stat = ""

    body_lines = [
        f"# Natural Language Coding hub v{ver}",
        "",
        "## Highlights",
        "",
        f"<!-- {HIGHLIGHTS_PLACEHOLDER} -->",
        "",
        heading,
        "",
    ]
    if commits:
        body_lines.extend(commits)
    else:
        body_lines.append("_No commits in range._")
    body_lines.append("")
    if stat:
        body_lines.extend(["### Diff stat", "", "```", stat, "```", ""])
    body_lines.extend(
        [
            "---",
            "",
            "Draft commits/range from "
            f"`python3 tools/nlc_release_notes.py --write-draft --version {ver} --to {to_ref}`. "
            "Edit **Highlights** before merge; `./release finish` refuses to tag without them.",
            "",
        ]
    )
    return "\n".join(body_lines)


_CHANGES_SECTION = re.compile(
    r"(?ms)^## Changes since v[\d.]+.*?(?=^---\s*$|\Z)",
)
_CHANGES_SECTION_ALT = re.compile(
    r"(?ms)^## Changes \(no prior semver tag in repo\).*?(?=^---\s*$|\Z)",
)


def refresh_changes_section(text: str, version: str, to_ref: str, from_tag: str | None) -> str:
    ver = version.lstrip("v")
    if from_tag:
        commits = commit_lines(from_tag, to_ref)
        heading = f"## Changes since {from_tag}"
        stat = diff_stat(from_tag, to_ref)
    else:
        proc = _git("log", to_ref, "--pretty=format:- %s (`%h`)", "-n", "50")
        commits = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]
        heading = "## Changes (no prior semver tag in repo)"
        stat = ""

    block_lines = [heading, ""]
    if commits:
        block_lines.extend(commits)
    else:
        block_lines.append("_No commits in range._")
    block_lines.append("")
    if stat:
        block_lines.extend(["### Diff stat", "", "```", stat, "```", ""])
    new_block = "\n".join(block_lines)

    if _CHANGES_SECTION.search(text):
        return _CHANGES_SECTION.sub(new_block + "\n", text, count=1)
    if _CHANGES_SECTION_ALT.search(text):
        return _CHANGES_SECTION_ALT.sub(new_block + "\n", text, count=1)
    # Append if structure unexpected
    return text.rstrip() + "\n\n" + new_block + "\n"


def highlights_body(text: str) -> str:
    match = re.search(r"(?ms)^## Highlights\s*\n(.*?)(?=^## |\Z)", text)
    if not match:
        return ""
    body = match.group(1)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    return body.strip()


def check_notes(version: str) -> tuple[bool, str]:
    path = notes_path(version)
    if not path.is_file():
        return False, f"missing file: {path.relative_to(ROOT)}"
    text = path.read_text(encoding="utf-8")
    if f"v{version.lstrip('v')}" not in text.splitlines()[0]:
        return False, "title line should be '# Natural Language Coding hub vX.Y.Z'"
    hi = highlights_body(text)
    if not hi:
        return False, "Highlights section is empty (remove placeholder comment and write summary)"
    if HIGHLIGHTS_PLACEHOLDER in hi or hi.startswith("<!--"):
        return False, "Highlights still contains placeholder — write user-facing summary"
    if len(hi) < 24:
        return False, "Highlights too short — add a real summary (adopters read this)"
    return True, "ok"


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Hub release notes helper")
    parser.add_argument("--version", metavar="X.Y.Z", help="Release version (no v prefix)")
    parser.add_argument("--to", dest="to_ref", default="HEAD", help="Git ref for range end")
    parser.add_argument("--from-tag", help="Override previous tag (default: latest before --version)")
    parser.add_argument("--previous-tag", action="store_true", help="Print previous tag and exit")
    parser.add_argument("--write-draft", action="store_true", help="Write draft file if missing")
    parser.add_argument("--force", action="store_true", help="Overwrite file with full draft")
    parser.add_argument("--refresh-changes", action="store_true", help="Update Changes section only")
    parser.add_argument("--check", action="store_true", help="Validate Highlights; exit 1 if not met")
    parser.add_argument("--print-draft", action="store_true", help="Print draft to stdout")
    args = parser.parse_args()

    if args.previous_tag:
        if not args.version:
            print("error: --version required", file=sys.stderr)
            return 2
        prev = changelog_base_tag(args.version, args.to_ref)
        if prev:
            print(prev)
        return 0

    if not args.version:
        parser.print_help()
        return 2

    from_tag = args.from_tag or changelog_base_tag(args.version, args.to_ref)
    if from_tag and not tag_exists(from_tag):
        from_tag = None

    if args.print_draft:
        print(build_draft(args.version, args.to_ref, from_tag))
        return 0

    path = notes_path(args.version)

    if args.write_draft or args.force:
        if path.is_file() and not args.force:
            print(f"exists: {path.relative_to(ROOT)} (use --force to replace)")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                build_draft(args.version, args.to_ref, from_tag),
                encoding="utf-8",
            )
            print(f"wrote: {path.relative_to(ROOT)}")
        return 0

    if args.refresh_changes:
        if not path.is_file():
            print(f"missing: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8")
        path.write_text(
            refresh_changes_section(text, args.version, args.to_ref, from_tag),
            encoding="utf-8",
        )
        print(f"refreshed changes: {path.relative_to(ROOT)}")
        return 0

    if args.check:
        ok, msg = check_notes(args.version)
        if ok:
            print(f"RELEASE_NOTES:MET {path.relative_to(ROOT)}")
            return 0
        print(f"RELEASE_NOTES:NOT_MET {msg}", file=sys.stderr)
        return 1

    parser.print_help()
    return 2


