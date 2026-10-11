#!/usr/bin/env python3
"""FINDINGS ship/tag prose must match reachable git tags on HEAD (F1)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = ROOT / "FINDINGS.md"

# Hand-written tag *existence* claims (must not appear in FINDINGS prose).
HAND_WRITTEN_TAG = re.compile(
    r"(tagged\s+on\s+origin|"
    r"Shipped\s+git\s+tag\s*:\s*v?\d+\.\d+\.\d+|"
    r"(?:Hub\s+)?no\s+shipped\s+tag|"
    r"v(\d+\.\d+\.\d+)\s+is\s+tagged|"
    r"tagged\s+on\s+origin.*v(\d+\.\d+\.\d+)|"
    r"v(\d+\.\d+\.\d+)\s+.*\bon\s+origin\b)",
    re.I,
)

# Lines that document the gate without asserting tag state.
GATE_DOC_ONLY = re.compile(
    r"(fitness-findings-shipped-tag-sync\.py|nlc_release_tags\.py|"
    r"generate from git only|Machine SSOT|do not hand-write origin tag claims|"
    r"never hand-write|fitness-findings-shipped-tag-sync)",
    re.I,
)


def main() -> int:
    _ = sys.argv[1:]
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_release_tags import last_shipped_tag, tag_version  # noqa: E402

    if not FINDINGS.is_file():
        print("VIOLATION missing FINDINGS.md")
        print("RESULT:NOT_MET")
        return 1

    raw = FINDINGS.read_text(encoding="utf-8", errors="replace")
    # Ignore SSOT instruction lines (they mention forbidden patterns literally).
    text = "\n".join(
        ln
        for ln in raw.splitlines()
        if "never hand-write" not in ln.lower() and "do not hand-write" not in ln.lower()
    )
    shipped = last_shipped_tag("HEAD")
    shipped_ver = tag_version(shipped) if shipped else None

    violations: list[str] = []
    for num, line in enumerate(text.splitlines(), start=1):
        if GATE_DOC_ONLY.search(line):
            continue
        m = HAND_WRITTEN_TAG.search(line)
        if not m:
            continue
        claimed = None
        for g in m.groups():
            if g and re.match(r"\d+\.\d+\.\d+", g):
                claimed = g
                break
        if claimed:
            if shipped_ver is None:
                violations.append(
                    f"FINDINGS line {num}: claims v{claimed} tag state but no reachable v*.*.* tag on HEAD"
                )
            elif claimed != shipped_ver:
                violations.append(
                    f"FINDINGS line {num}: claims v{claimed} but newest reachable tag is v{shipped_ver}"
                )
        else:
            violations.append(
                f"FINDINGS line {num}: hand-written tag existence prose (use git tag / fitness only)"
            )

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())


BOUNDARY = "bba-emit"
