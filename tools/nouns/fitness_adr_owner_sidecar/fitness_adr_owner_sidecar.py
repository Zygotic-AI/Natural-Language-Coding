"""ADR 0052 step 2: OpenPGP sidecar required for every Accepted document (C6)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import subprocess
import sys
from pathlib import Path

from nouns.owner_sidecar.owner_sidecar import verify_sidecar_p1

_STATUS = re.compile(r"^-?\s*Status:\s*(\S+)", re.M)
_ADR_FILE = re.compile(r"^(\d{4})-.+\.md$")
_SKIP_PREFIXES = (
    "tools/fixtures/",
    "examples/",
    "docs/history/",
    "docs/rca/",
    "reviews/",
)


def _git_tracked_files(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [line.strip().replace("\\", "/") for line in (proc.stdout or "").splitlines() if line.strip()]


def _status_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = _STATUS.search(text)
    return match.group(1) if match else ""


def accepted_document_rels(root: Path) -> list[str]:
    """Every Accepted document. ACTIVE.md membership does not matter. Fixtures/examples excluded."""
    found: list[str] = []
    adrs = root / "adrs"
    if adrs.is_dir():
        for path in sorted(adrs.glob("[0-9][0-9][0-9][0-9]-*.md")):
            if _status_of(path) == "Accepted":
                found.append(path.relative_to(root).as_posix())
    for rel in _git_tracked_files(root):
        if not rel.endswith(".md"):
            continue
        if any(rel.startswith(prefix) for prefix in _SKIP_PREFIXES):
            continue
        if rel.startswith("adrs/") and _ADR_FILE.match(Path(rel).name):
            continue
        path = root / rel
        if not path.is_file():
            continue
        if _status_of(path) == "Accepted":
            found.append(rel)
    return sorted(set(found))


def sidecar_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in accepted_document_rels(root):
        errors.extend(verify_sidecar_p1(root, rel))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = sidecar_errors(root)
    if errors:
        for item in errors[:30]:
            print(f"VIOLATION {item}")
        if len(errors) > 30:
            print(f"VIOLATION ... and {len(errors) - 30} more")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
