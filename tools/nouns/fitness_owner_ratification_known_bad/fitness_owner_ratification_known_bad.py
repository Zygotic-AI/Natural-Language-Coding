"""ADR 0051/0052 known-bad Candidates verified directly (P6)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIX = ROOT / "tools" / "fixtures" / "owner-ratification-sidecar"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.hub_own_produce.hub_own_produce import validate_hub_material_fixture
    from nouns.owner_sidecar.owner_sidecar import verify_sidecar_p1, verify_sidecar_p1_on_bytes
    from nouns.fitness_owner_key_trust.fitness_owner_key_trust import key_trust_errors

    violations: list[str] = []

    unsigned_rel = "tools/fixtures/owner-ratification-sidecar/accepted-doc-no-sidecar.md"
    unsigned_errors = verify_sidecar_p1(ROOT, unsigned_rel)
    if not unsigned_errors:
        violations.append("unsigned Accepted doc: expected NOT_MET got MET")

    cases_path = FIX / "cases.json"
    if not cases_path.is_file():
        violations.append("missing cases.json")
    else:
        from nouns.owner_sidecar.owner_sidecar import statement_field_errors

        for case in json.loads(cases_path.read_text(encoding="utf-8")):
            name = case["name"]
            doc_rel = case["document_rel"]
            doc_bytes = (ROOT / doc_rel).read_bytes()
            status = case["status"]
            mode = case.get("mode", "sidecar")
            if mode == "fields":
                errs = statement_field_errors(
                    case["fields"], document_rel=doc_rel, document_bytes=doc_bytes, status=status
                )
            else:
                asc = ROOT / case["sidecar_rel"]
                errs = verify_sidecar_p1_on_bytes(
                    ROOT,
                    document_rel=doc_rel,
                    document_bytes=doc_bytes,
                    asc_path=asc,
                    status=status,
                )
            if case.get("expect_not_met", True):
                if not errs:
                    violations.append(f"{name}: expected NOT_MET got MET")
            else:
                if errs:
                    violations.append(f"{name}: expected MET got {errs}")

    from nouns.fitness_owner_key_trust.fitness_owner_key_trust import _trusted_before, _merge_base, DEFAULT_BASE_REF
    from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL
    from nouns.owner_sidecar.owner_sidecar import sidecar_path_for_document, verify_sidecar_with_trusted_set
    import tempfile

    base_rev = _merge_base(ROOT, DEFAULT_BASE_REF)
    if base_rev:
        trusted_before, _ = _trusted_before(ROOT, base_rev)
        wrong_asc = FIX / "manifest-wrong-key.approval.asc"
        if wrong_asc.is_file() and trusted_before:
            with tempfile.TemporaryDirectory() as tmp:
                from nouns.fitness_owner_key_trust.fitness_owner_key_trust import _git_show, OWNER_KEY_REL
                base_key = _git_show(ROOT, base_rev, OWNER_KEY_REL)
                if base_key:
                    kp = Path(tmp) / "base.asc"
                    kp.write_bytes(base_key)
                    errs = verify_sidecar_with_trusted_set(
                        ROOT,
                        MANIFEST_REL,
                        wrong_asc,
                        trusted_fingerprints=trusted_before,
                        key_import_paths=[kp],
                    )
                    if not errs:
                        violations.append("key-rotation-wrong-signer: expected NOT_MET got MET")

    ci_fixture = ROOT / "tools/fixtures/hub-own/invalid-hub-own-ci-only-exit.json"
    data = json.loads(ci_fixture.read_text(encoding="utf-8"))
    data = {k: v for k, v in data.items() if not str(k).startswith("_")}
    ok, reason = validate_hub_material_fixture(data, "property_exit")
    if ok:
        violations.append(f"ci-only-exit: expected NOT_MET got pass ({reason})")

    from nouns.gate_set_manifest.gate_set_manifest import fixture_edit_would_break_manifest, path_in_manifest_holds

    fixture_rel = "tools/fixtures/hub-own/valid-hub-own-produce-package.json"
    fixture_path = ROOT / fixture_rel
    if not path_in_manifest_holds(ROOT, fixture_rel):
        violations.append("fixture-edit-manifest: specimen not in ratified manifest")
    elif fixture_path.is_file():
        tampered = fixture_path.read_bytes() + b"\n# gate-set fixture tamper\n"
        if not fixture_edit_would_break_manifest(ROOT, fixture_rel, tampered):
            violations.append("fixture-edit-manifest: tampered fixture should break manifest")

    gate_set_cases = ROOT / "tools/fixtures/owner-ratification-gate-set/cases.json"
    if not gate_set_cases.is_file():
        violations.append("missing tools/fixtures/owner-ratification-gate-set/cases.json")
    else:
        from nouns.gate_set_manifest.gate_set_manifest import gate_set_manifest_errors

        for case in json.loads(gate_set_cases.read_text(encoding="utf-8")):
            name = case["name"]
            rel = case["document_rel"]
            doc = ROOT / rel
            if not doc.is_file():
                violations.append(f"{name}: missing {rel}")
                continue
            suffix = case.get("tamper_suffix", "# tamper\n").encode("utf-8")
            tampered = doc.read_bytes() + suffix
            errs = gate_set_manifest_errors(ROOT, overrides={rel: tampered})
            if not errs:
                violations.append(f"{name}: tampered {rel} expected NOT_MET got MET")

    gate_subject = ROOT / "tools/fixtures/hub-own/invalid-hub-own-gate-subject-same-actor.json"
    gs = json.loads(gate_subject.read_text(encoding="utf-8"))
    gs = {k: v for k, v in gs.items() if not str(k).startswith("_")}
    from nouns.hub_own_produce.hub_own_produce import validate_hub_gate_diff_role_separation

    ok_gs, reason_gs = validate_hub_gate_diff_role_separation(ROOT, gs)
    if ok_gs:
        violations.append(f"gate-subject-same-actor: expected NOT_MET got pass ({reason_gs})")

    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
