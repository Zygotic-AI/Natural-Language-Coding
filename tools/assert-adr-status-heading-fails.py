#!/usr/bin/env python3
"""Known-bad: heading/bold/unparseable Status must fail C6 closed."""
from __future__ import annotations

import shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tools/fixtures/owner-ratification-sidecar"
CASES = (
    ("9998-heading-status-accepted.md", "adrs/9998", "missing sidecar", True),
    ("9997-unparseable-status.md", "adrs/9997", "unparseable or unknown Status", False),
    ("9996-bold-status-accepted.md", "adrs/9996", "missing sidecar", True),
)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        w = Path(tmp) / "r"
        subprocess.run(["git", "clone", "--local", "-q", str(ROOT), str(w)], check=True)
        head = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
        subprocess.run(["git", "-C", str(w), "checkout", "-q", head], check=True)
        sys.path.insert(0, str(w / "tools"))
        from nouns.fitness_adr_owner_sidecar import fitness_adr_owner_sidecar as m

        ok = True
        for name, needle, expect, must_count in CASES:
            for leftover in (w / "adrs").glob("999[678]-*.md"):
                leftover.unlink()
            shutil.copy(FIX / name, w / "adrs" / name)
            subprocess.run(["git", "-C", str(w), "add", "-A"], check=True)
            counted = any(r.startswith(needle) for r in m.accepted_document_rels(w))
            errs = [e for e in m.sidecar_errors(w) if needle in e]
            good = bool(errs) and any(expect in e for e in errs)
            if must_count:
                good = good and counted
            print(f"{'PASS' if good else 'FAIL'} {name}: counted={counted} errors={errs[:1]}")
            print(f"ASSERT:{'PASS' if good else 'FAIL'} {name}")
            ok = ok and good
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
