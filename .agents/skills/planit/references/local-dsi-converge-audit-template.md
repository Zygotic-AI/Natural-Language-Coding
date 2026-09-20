# `/local-dsi-converge` [audit](../../../../docs/TERMS.md#audit) template

Copy into `$CONSUMER_REPO/doc/LOCAL-DSI-CONVERGE-AUDIT.md` after each converge. Normative contracts: [`dsi-converge-deliverable-contract.md` (dsi-converge-deliverable-contract.md — not bundled in this skill).

**[AWL](../../../../docs/TERMS.md#awl) mapping:** This template is a **Phase 6 execution-audit instance** of the org-wide [`audited-work-loop-standard.md`](audited-work-loop-standard.md) (adversarial execution audit with machine gates and spot checks). It is not a separate process from [AWL](../../../../docs/TERMS.md#awl).

---

## Apex (required)

| Field | Value |
| ----- | ----- |
| **Lens A — Machine converge** | **100% PASS** or **FAIL** |
| **Re-run `/local-dsi-converge` required? (lens A only)** | **Yes** / **No** |
| **Deliverable [contract](../../../../docs/TERMS.md#contract) recorded** | `machine_converge_v1` / `consumer_dsi_full_v1` |
| **Lens B — Full consumer SKILL** | **100% PASS** or **NOT 100% PASS** (only if contract = `consumer_dsi_full_v1`) |
| **Lens C — Strict advisories** | **100% PASS** or **NOT 100% PASS** (only if audit used `--audit-strict-caveats`) |
| **DSI-RECHECK.md [action](../../../../docs/TERMS.md#action)** | **None** / **Remove row** (remove only if lens A PASS **and** lens C PASS when strict caveats opted in) |

**Why (one breath):** …

**Next [action](../../../../docs/TERMS.md#action):** …

---

## Labels

| Label | Meaning |
| ----- | ------- |
| **100% PASS** | Exit **0**, zero hard errors, zero blocking predicates for that stage’s scope. |
| **NOT 100% PASS** | Scope not fully [met](../../../../docs/TERMS.md#met); ≠ machine **FAIL** unless lens A says **FAIL**. |
| **FAIL** | Hard failure on final tree or lens A violated. |

---

## Stage register

(Fill one row per stage: G0, G1, G2, O0, A, A′, B, C′, C, CTQ, F, D, SC1–SC8, Q-ADV, E, E-NAR, H, UP — mark **100% PASS** or **NOT 100% PASS** per lens columns in [`dsi-converge-deliverable-contract.md` (dsi-converge-deliverable-contract.md — not bundled in this skill).)

---

## Iron-clad process [RCA](../../../../docs/TERMS.md#rca) (consolidated)

| Gap IDs | Process root | Iron-clad vault fix |
| ------- | ------------ | ------------------- |
| A′, F, E-NAR (lens B) | **P1** Deliverable [contract](../../../../docs/TERMS.md#contract) split | `--deliverable-contract consumer_dsi_full_v1` + [handoff](../../../../docs/TERMS.md#handoff) gates |
| Q-ADV (lens C) | **P2** [Audit](../../../../docs/TERMS.md#audit) vs stop predicate mismatch | Lens A only for RECHECK; lens C opt-in |
| Q-ADV (ETL shape) | **P3** Extract-or-slot advisories | Not a machine [defect](../../../../docs/TERMS.md#defect); no re-converge for ratios alone |

Per-stage RCAs must map to **P1**, **P2**, or **P3** — not ad-hoc “re-run converge” without [contract](../../../../docs/TERMS.md#contract) change.

---

## Re-verification commands

```bash
VENV_PY="/path/to/tools/tree-sitter/.venv/bin/python"
SKILL_DIR="/path/to/ai/skills/document-service-integrations"
REPO="/path/to/consumer"
SVC="munibatch"
export DSI_TREESITTER_PYTHON="$VENV_PY"
"$VENV_PY" "$SKILL_DIR/scripts/converge/process_gates.py" --repo "$REPO" --probe-writable
"$VENV_PY" "$SKILL_DIR/scripts/converge/process_gates.py" --repo "$REPO" --assert-ownership
"$VENV_PY" "$SKILL_DIR/scripts/converge/stop_check.py" --repo "$REPO" --output doc/integrations \
  --deliverable-contract consumer_dsi_full_v1
"$VENV_PY" "$SKILL_DIR/scripts/validate_integrations_audit.py" --repo "$REPO" --output doc/integrations
"$VENV_PY" "$SKILL_DIR/scripts/converge/completeness_audit.py" --service-dir "$REPO/doc/integrations/$SVC"
"$VENV_PY" "$SKILL_DIR/scripts/converge/sql_ipo_fidelity_audit.py" --service-dir "$REPO/doc/integrations/$SVC"
python3 -c "import json; from pathlib import Path; db=json.loads(Path('$REPO/doc/integrations/$SVC/database-calls.json').read_text()); print('empty connectionSource', sum(1 for e in db if not (e.get('connectionSource') or '').strip()), '/', len(db))"
```

### Dual-audit metrics (record in stage register)

| Metric | Target (`consumer_dsi_full_v1`) |
| ------ | ------------------------------- |
| `completeness_audit` gap count | **0** |
| `sql_ipo_fidelity_audit` mismatch count | **0** |
| Empty `connectionSource` in `database-calls.json` | **0** |

---

## References

- Converge log: `doc/integrations/_converge/YYYY-MM-DD-*.json`
- Standard: [`dsi-converge-deliverable-contract.md` (dsi-converge-deliverable-contract.md — not bundled in this skill)
