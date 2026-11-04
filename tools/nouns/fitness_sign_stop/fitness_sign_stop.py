"""KB-0058-sign-stop: release docs and the /release skill must not tell a human to sign."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SURFACES = (
    ROOT / "docs" / "adoption" / "RELEASE.md",
    ROOT / ".agents" / "skills" / "release" / "SKILL.md",
    ROOT / "docs" / "nlc" / "HUMAN-JUDGMENT-GATES.md",
)
FORBIDDEN = (
    "sign this",
    "clearsign",
    "owner must sign",
    "please sign",
    "gpg sidecar",
    "unsigned produce is incomplete",
    "unsigned manifest is incomplete",
)


def sign_stop_errors(root: Path) -> list[str]:
    """NOT_MET when a release surface tells the human to sign."""
    errors: list[str] = []
    for path in (
        root / "docs" / "adoption" / "RELEASE.md",
        root / ".agents" / "skills" / "release" / "SKILL.md",
        root / "docs" / "nlc" / "HUMAN-JUDGMENT-GATES.md",
    ):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(root).as_posix()}")
            continue
        text = path.read_text(encoding="utf-8").lower()
        for needle in FORBIDDEN:
            if needle in text:
                errors.append(f"{path.relative_to(root).as_posix()} tells the human to sign ({needle!r})")
    return errors


def main() -> int:
    errors = sign_stop_errors(ROOT)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
