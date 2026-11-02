"""Known-bad: a hand edit to FINDINGS or DESCRIBE fails the script-match check."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


def _copy_surface(tmp: Path, rel: str) -> None:
    dest = tmp / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes((ROOT / rel).read_bytes())


def main() -> int:
    from nouns.release_prep_surfaces.release_prep_surfaces import (
        DESCRIBE_REL,
        FINDINGS_REL,
        RECORD_REL,
        VERSION_REL,
        match_errors,
    )

    tmp = Path(tempfile.mkdtemp())
    for rel in (FINDINGS_REL, DESCRIBE_REL, RECORD_REL, VERSION_REL):
        _copy_surface(tmp, rel)
    clean = match_errors(tmp)
    if clean:
        return _fail(f"clean copy should match script output: {clean}")

    version = json.loads((tmp / VERSION_REL).read_text(encoding="utf-8"))["version"]
    findings = (tmp / FINDINGS_REL).read_text(encoding="utf-8")
    needle = f"Shipped git tag **`v{version}`**"
    if needle not in findings:
        return _fail(f"FINDINGS missing {needle!r} for the hand-edit landmine")
    (tmp / FINDINGS_REL).write_text(
        findings.replace(needle, "Shipped git tag **`v0.0.0`**", 1),
        encoding="utf-8",
    )
    bad_findings = match_errors(tmp)
    if not bad_findings:
        return _fail("hand-edited FINDINGS matched script output")

    _copy_surface(tmp, FINDINGS_REL)
    describe = (tmp / DESCRIBE_REL).read_text(encoding="utf-8")
    (tmp / DESCRIBE_REL).write_text(
        describe.replace(f"v{version}", "v0.0.0", 1),
        encoding="utf-8",
    )
    bad_describe = match_errors(tmp)
    if not bad_describe:
        return _fail("hand-edited DESCRIBE matched script output")
    print("ASSERT:PASS hand edit to FINDINGS/DESCRIBE fails script-match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
