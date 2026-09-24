# Inference phases (full NLC audit)

Machine stages run via `python3 tools/full-nlc-audit.py --check`. These phases are **agent-executed** after machine `FULL_NLC_AUDIT:MET` (or in parallel when diagnosing machine FAIL).

## Phase 0 — Recon

1. Record exact commit SHA audited.
2. Map the tree: `CHARTER.md`, `DESCRIBE.md`, `FINDINGS.md`, `HOLES.md`, `TODO`, `docs/USE-CASES.md`, `docs/TERMS.md`, `docs/nlc/*`, `adrs/`, `.agents/skills/`, `agents/`, `tools/`, `MANIFESTO.md`, `integrity/binding-matrix.json`, `integrity/integration-leaves.json`.
3. Count ADRs in `adrs/ACTIVE.md`. Note Accepted vs parked.
4. Run binding matrix summary from machine stage output or `python3 tools/audit-binding-matrix.py`.

## Phase 1 — Roof consistency (ADR 0011)

- `CHARTER.md` / `DESCRIBE.md` / README — NLC-first consumer door
- No BBA/BBP roof leakage in GETTING-STARTED
- Manifesto six principles + layer stack

## Phase 2 — Gap tracker SSOT

- `FINDINGS.md` sole live queue; `TODO` is log not second queue
- Last pass SHA vs HEAD
- Stale FINDINGS rows

## Phase 3 — Binding matrix buckets

Classify unbound rules: structural vs semantic vs process (C24).

## Phase 4 — Ratification coverage

Charter rules vs per-rule ADRs (ADR 0031 program + backlog).

## Phase 5 — Soft-green honesty

Compile ≠ ship; Accepted ADR ≠ wired gate; Python-first language honesty.

## Phase 6 — Product continuity

Cross-check FINDINGS Needed/Parked vs `integrity/uc-product-status.json` vs `docs/USE-CASES.md`.

## Phase 7 — Integration leaves

For each row in `integrity/integration-leaves.json`: disposition matches tree (no orphan partials).

## Report sections

1. Audit metadata (SHA, date)
2. Machine stage register (from `full-nlc-audit.py` output)
3. Coverage summary
4. Findings (ID, severity, evidence, remediation suggestion)
5. Soft-green residuals
