#!/usr/bin/env python3
"""BBP binding-matrix audits: coverage, unbound list, promote/bindable list.

Input: no argv. Scans hub trees via fixed paths:
  integrity/binding-matrix.json, CHARTER.md, integrity/PRINCIPLES.md
  (no domain/goals scan).

Output: lines among
  A-BINDING-COVERAGE:MET|NOT_MET
  A-BINDING-UNBOUND:MET|NOT_MET
  A-BINDING-PROMOTE:MET|NOT_MET
  MISSING_FROM_MATRIX <id>
  MISSING_AUDIT_ID <id>
  UNBOUND <id>          (in-force unbound only)
  IN_FORCE_UNBINDABLE <id>
  RESULT:MET|NOT_MET
  and on NOT_MET, the failing audit name lines again.

Failure mode: process exit 0 = RESULT:MET (PASS); exit 1 = RESULT:NOT_MET (FAIL).
  Does not swallow exceptions silently — unexpected errors propagate and abort.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "integrity" / "binding-matrix.json"
CHARTER_PATH = ROOT / "CHARTER.md"
PRINCIPLES_PATH = ROOT / "integrity" / "PRINCIPLES.md"


def load_matrix():
    return json.loads(MATRIX_PATH.read_text())


def published_ids():
    ids = set()
    charter = CHARTER_PATH.read_text()
    ids.update(re.findall(r"\*\*(R\d+)\.\*\*", charter))
    ids.update(re.findall(r"\*\*(R\d+)\.\*\*", CHARTER_PATH.read_text()))
    ids.update(re.findall(r"- \[ \] (C\d+)\.", charter))
    # R26+ may use ### headings or **R26.** after charter amend
    ids.update(re.findall(r"\*\*(R2[6-9]|R3\d)\.\*\*", charter))
    principles = PRINCIPLES_PATH.read_text()
    ids.update(re.findall(r"^## (P\d+) —", principles, re.M))
    return ids


def main():
    matrix = load_matrix()
    rows = matrix["requirements"]
    by_id = {r["id"]: r for r in rows}
    failures = []

    # A-BINDING-COVERAGE
    missing = sorted(published_ids() - set(by_id))
    no_audit = sorted(
        r["id"] for r in rows if not str(r.get("audit_id") or "").strip()
    )
    if missing or no_audit:
        failures.append("A-BINDING-COVERAGE:NOT_MET")
        for i in missing:
            print(f"MISSING_FROM_MATRIX {i}")
        for i in no_audit:
            print(f"MISSING_AUDIT_ID {i}")
    else:
        print("A-BINDING-COVERAGE:MET")

    # A-BINDING-UNBOUND — only in-force rows must be bound
    unbound = []
    for r in rows:
        if r.get("surface") != "in-force":
            continue
        binder = str(r.get("binder") or "").strip()
        if r.get("status") == "unbound" or not binder:
            unbound.append(r["id"])
    unbound = sorted(set(unbound))
    if unbound:
        failures.append("A-BINDING-UNBOUND:NOT_MET")
        for i in unbound:
            print(f"UNBOUND {i}")
    else:
        print("A-BINDING-UNBOUND:MET")

    # A-BINDING-PROMOTE
    unbindable_in_force = []
    for r in rows:
        if r.get("surface") != "in-force":
            continue
        binder = str(r.get("binder") or "").strip()
        if r.get("status") != "bound" or not binder:
            unbindable_in_force.append(r["id"])
    unbindable_in_force = sorted(set(unbindable_in_force))
    if unbindable_in_force:
        failures.append("A-BINDING-PROMOTE:NOT_MET")
        for i in unbindable_in_force:
            print(f"IN_FORCE_UNBINDABLE {i}")
    else:
        print("A-BINDING-PROMOTE:MET")

    if failures:
        print("RESULT:NOT_MET")
        for f in failures:
            print(f)
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
