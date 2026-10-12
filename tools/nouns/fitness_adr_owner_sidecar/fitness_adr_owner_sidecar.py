"""ADR 0052 P1/P2: OpenPGP sidecar for Accepted ADRs > 0051; legacy report for <= 0051."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

from nouns.adr_approval.adr_approval import active_numbers
from nouns.owner_sidecar.owner_sidecar import verify_sidecar_p1

REPORT_REL = "integrity/adr-openpgp-legacy-report.txt"
_STATUS = re.compile(r"^-\s*Status:\s*(\S+)", re.M)


def _adr_file(root: Path, number: str) -> Path | None:
    matches = sorted((root / "adrs").glob(f"{number}-*.md"))
    if len(matches) != 1:
        return None
    return matches[0]


def _adr_int(number: str) -> int:
    return int(number)


def sidecar_errors(root: Path) -> list[str]:
    errors: list[str] = []
    legacy_lines: list[str] = []
    for number in active_numbers((root / "adrs" / "ACTIVE.md").read_text(encoding="utf-8")):
        path = _adr_file(root, number)
        if path is None:
            errors.append(f"{number}: ADR file missing")
            continue
        text = path.read_text(encoding="utf-8")
        status_match = _STATUS.search(text)
        status = status_match.group(1) if status_match else ""
        if status != "Accepted":
            continue
        n = _adr_int(number)
        if n <= 51:
            legacy_lines.append(f"{number} unsigned (legacy hash receipt)")
            continue
        errors.extend(verify_sidecar_p1(root, str(path.relative_to(root).as_posix())))
    report_path = root / REPORT_REL
    expected_report = "\n".join(legacy_lines) + ("\n" if legacy_lines else "")
    if not report_path.is_file():
        errors.append(f"missing {REPORT_REL}")
    elif report_path.read_text(encoding="utf-8") != expected_report:
        errors.append(f"{REPORT_REL} stale (run tools/generate-adr-openpgp-legacy-report.py)")
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
