"""C5: every rules-SSOT constraint has a known-bad Candidate that the constraint refuses."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

from nouns.fitness_adr_0051_0052_rules.fitness_adr_0051_0052_rules import (
    OWNER_EXEMPT,
    load_rules,
)
from nouns.hub_own_produce.hub_own_produce import (
    validate_hub_brief,
    validate_hub_exit_not_ci_only,
    validate_hub_gate_diff_role_separation,
    validate_hub_material_package,
    validate_property_leaf_goals,
)
from nouns.owner_sidecar.owner_sidecar import (
    pending_presented_as_ratified_errors,
    verify_sidecar_p1,
)
from nouns.fitness_no_check_on_check.fitness_no_check_on_check import (
    check_on_check_errors_for_source,
)
from nouns.fitness_no_tool_writes_ratification.fitness_no_tool_writes_ratification import (
    ratification_write_errors_for_source,
)
from nouns.fitness_retired_key_denylist.fitness_retired_key_denylist import retired_key_errors
from nouns.fitness_adr_0051_0052_rules.fitness_adr_0051_0052_rules import rules_ssot_errors
from nouns.adr_record_gate.adr_record_gate import constraint_row_errors

ROOT = Path(__file__).resolve().parents[3]
CASES_REL = "integrity/known-bad-cases.json"
RULES_REL = "integrity/adr-0051-0052-rules.json"
KNOWN_BAD = ROOT / "tools/fixtures/known-bad-ssot/missing-constraint-entry.json"


def _load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _strip(data: dict[str, object]) -> dict[str, object]:
    return {k: v for k, v in data.items() if not str(k).startswith("_")}


def _not_met(ok: bool, reason: str, needle: str) -> list[str]:
    if ok:
        return [f"expected NOT_MET got MET ({reason})"]
    if needle and needle not in reason:
        return [f"expected reason {needle!r} got {reason!r}"]
    return []


def run_constraint_verify(root: Path, case: dict[str, object]) -> list[str]:
    """Run the named constraint's own verify on the Candidate. Returns [] when NOT_MET as required."""
    kind = str(case.get("verify_kind") or "")
    candidate = str(case.get("candidate") or "")
    needle = str(case.get("expected_reason_substring") or "")
    path = root / candidate if candidate else None
    if kind == "hub_material_package":
        data = _strip(json.loads(path.read_text(encoding="utf-8"))) if path and path.is_file() else {}
        ok, _kind, reason = validate_hub_material_package(root, data)
        return _not_met(ok, reason, needle)
    if kind == "property_leaves":
        data = _strip(json.loads(path.read_text(encoding="utf-8"))) if path and path.is_file() else {}
        ok, reason = validate_property_leaf_goals(data)
        return _not_met(ok, reason, needle)
    if kind == "hub_exit":
        data = _strip(json.loads(path.read_text(encoding="utf-8"))) if path and path.is_file() else {}
        ok, reason = validate_hub_exit_not_ci_only(data)
        return _not_met(ok, reason, needle)
    if kind == "hub_brief":
        data = _strip(json.loads(path.read_text(encoding="utf-8"))) if path and path.is_file() else {}
        ok, reason = validate_hub_brief(root, data)
        return _not_met(ok, reason, needle)
    if kind == "role_separation":
        data = _strip(json.loads(path.read_text(encoding="utf-8"))) if path and path.is_file() else {}
        ok, reason = validate_hub_gate_diff_role_separation(root, data)
        return _not_met(ok, reason, needle)
    if kind == "sidecar_p1":
        errs = verify_sidecar_p1(root, candidate)
        if not errs:
            return ["expected sidecar NOT_MET got MET"]
        blob = " ".join(errs)
        if needle and needle not in blob:
            return [f"expected reason {needle!r} got {blob!r}"]
        return []
    if kind == "pending_ratified":
        payload = json.loads(path.read_text(encoding="utf-8")) if path and path.is_file() else []
        rows = payload if isinstance(payload, list) else payload.get("cases") if isinstance(payload, dict) else []
        if not isinstance(rows, list) or not rows:
            return ["pending candidate missing cases"]
        first = rows[0]
        if not isinstance(first, dict):
            return ["pending case must be object"]
        fields = {str(k): str(v) for k, v in dict(first.get("fields") or {}).items()}
        found = pending_presented_as_ratified_errors(
            str(first.get("status") or ""), fields, document_rel=str(first.get("document_rel") or "")
        )
        if not found:
            return ["expected pending NOT_MET got MET"]
        blob = " ".join(found)
        if needle and needle not in blob:
            return [f"expected reason {needle!r} got {blob!r}"]
        return []
    if kind == "no_check_on_check":
        source = path.read_text(encoding="utf-8") if path and path.is_file() else ""
        found = check_on_check_errors_for_source(candidate, source)
        if not found:
            return ["expected check-on-check NOT_MET got MET"]
        blob = " ".join(found)
        if needle and needle not in blob:
            return [f"expected reason {needle!r} got {blob!r}"]
        return []
    if kind == "no_tool_writes":
        source = path.read_text(encoding="utf-8") if path and path.is_file() else ""
        found = ratification_write_errors_for_source(candidate, source)
        if not found:
            return ["expected write-sidecar NOT_MET got MET"]
        blob = " ".join(found)
        if needle and needle not in blob:
            return [f"expected reason {needle!r} got {blob!r}"]
        return []
    if kind == "retired_key":
        retired = (root / "integrity/owner-keys/RETIRED_FINGERPRINTS").read_text(encoding="utf-8")
        trusted = path.read_text(encoding="utf-8") if path and path.is_file() else ""
        found = retired_key_errors(root, trusted_text=trusted, retired_text=retired)
        if not any("overlap" in item for item in found):
            return ["expected retired-key overlap NOT_MET"]
        return []
    if kind == "rules_ssot":
        payload = _load_json(path) if path and path.is_file() else {}
        found = rules_ssot_errors(root, payload)
        if not found:
            return ["expected rules SSOT NOT_MET got MET"]
        blob = " ".join(found)
        if needle and needle not in blob:
            return [f"expected reason {needle!r} got {blob!r}"]
        return []
    if kind == "adr_gates_constraints":
        payload = _load_json(path) if path and path.is_file() else {}
        found = constraint_row_errors(root, payload)
        if not found:
            return ["expected adr-gates constraint row NOT_MET got MET"]
        blob = " ".join(found)
        if needle and needle not in blob:
            return [f"expected reason {needle!r} got {blob!r}"]
        return []
    if kind == "gate_set_tamper":
        from nouns.gate_set_manifest.gate_set_manifest import gate_set_manifest_errors

        if path is None or not path.is_file():
            return [f"missing gate-set tamper candidate {candidate}"]
        tampered = path.read_bytes() + b"\n# gate-set known-bad tamper\n"
        found = gate_set_manifest_errors(root, overrides={candidate: tampered})
        if not found:
            return ["expected gate-set tamper NOT_MET got MET"]
        blob = " ".join(found)
        if needle and needle not in blob:
            return [f"expected reason {needle!r} got {blob!r}"]
        return []
    if kind == "known_bad_ssot":
        found = known_bad_ssot_errors(root, _load_json(path) if path and path.is_file() else {})
        if not found:
            return ["expected known-bad SSOT NOT_MET got MET"]
        blob = " ".join(found)
        if needle and needle not in blob:
            return [f"expected reason {needle!r} got {blob!r}"]
        return []
    return [f"unknown verify_kind {kind!r}"]


def required_constraint_ids(root: Path) -> list[str]:
    rules = _load_json(root / RULES_REL)
    ids: list[str] = []
    for row in load_rules(rules):
        rid = str(row.get("id") or "")
        status = str(row.get("status") or "")
        if not rid or status == "CONTEXT" or rid in OWNER_EXEMPT:
            continue
        ids.append(rid)
    return ids


def known_bad_ssot_errors(root: Path, payload: dict[str, object] | None = None) -> list[str]:
    errors: list[str] = []
    if payload is None:
        path = root / CASES_REL
        if not path.is_file():
            return [f"missing {CASES_REL}"]
        payload = _load_json(path)
    cases = payload.get("cases")
    if not isinstance(cases, dict):
        return [f"{CASES_REL} cases must be object"]
    required = required_constraint_ids(root)
    for rid in required:
        if rid not in cases:
            errors.append(f"missing known-bad entry for {rid}")
    if errors:
        return errors
    for rid in required:
        case = cases.get(rid)
        if not isinstance(case, dict):
            errors.append(f"{rid}: case must be object")
            continue
        found = run_constraint_verify(root, case)
        for item in found:
            errors.append(f"{rid}: {item}")
    return errors


def main() -> int:
    errors = known_bad_ssot_errors(ROOT)
    if not KNOWN_BAD.is_file():
        errors.append(f"missing known-bad {KNOWN_BAD.relative_to(ROOT)}")
    else:
        kb = known_bad_ssot_errors(ROOT, _load_json(KNOWN_BAD))
        if not kb:
            errors.append("known-bad missing-constraint-entry.json: expected NOT_MET got MET")
    if errors:
        for item in errors[:40]:
            print(f"VIOLATION {item}")
        if len(errors) > 40:
            print(f"VIOLATION ... and {len(errors) - 40} more")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
