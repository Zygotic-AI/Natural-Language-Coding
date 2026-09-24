---
name: nlc-hub-audit
description: Legacy alias — use full-nlc-audit instead. Redirects to the single hub continuity entrypoint (machine manifest + inference phases).
disable-model-invocation: true
---

# NLC Hub Audit (alias)

**Use [`full-nlc-audit`](full-nlc-audit/SKILL.md)** — single entrypoint:

1. `python3 tools/full-nlc-audit.py --check --profile quick|full`
2. Inference phases in [`full-nlc-audit/references/inference-phases.md`](../full-nlc-audit/references/inference-phases.md)

This file remains for slash-command discovery only. Do not diverge checklists — edit `full-nlc-audit` SSOT.

---

# NLC Hub Audit (historical checklist)

You are auditing an NLC-shaped repository. Follow every phase in order. Do not skip phases. Do not invent findings outside the checklist. Record every finding with evidence (file path + line or section). The goal is that any agent running this skill produces the same findings for the same commit.

SSOT for this skill: `.agents/skills/full-nlc-audit/SKILL.md` (mirrored under `.cursor/skills` via symlink).

## Gate (default-closed)

Do **not** emit a findings report until every **blocking** row is true. Audit only — no remediations in the same turn.

| Criterion | Blocking? | Pass when | Evidence |
| --------- | --------- | --------- | -------- |
| SHA recorded | yes | Exact commit SHA (or unreachable stop) | Audit metadata |
| Phases 0–6 run in order | yes | Each phase has findings or explicit "no findings" | Report sections |
| Evidence cited | yes | Every finding has path + section/line | Findings list |
| No roof reopen | yes | Does not propose renaming public roof away from NLC | Hard rules |
| No same-turn fixes | yes | Report contains remediation *suggestions* only | Procedure |

**Done signals:** Report sections 1–6 present; Gate table all blocking rows true; soft-green residuals listed.

## Inputs

- Target repo URL or local path (default: https://github.com/Zygotic-AI/Natural-Language-Coding)
- Baseline SHA or ref (default: `main` HEAD; record the exact SHA you audited)
- Optional: prior findings list to diff against

## Phase 0 — Recon

1. Record exact commit SHA audited.
2. Map the tree: `CHARTER.md`, `DESCRIBE.md`, `FINDINGS.md`, `HOLES.md`, `TODO`, `USE-CASES.md`, `docs/TERMS.md`, `docs/nlc/*`, `adrs/`, `.agents/skills/`, `agents/`, `tools/`, `MANIFESTO.md`, `docs/nlc/compiler/MANIFESTO.md`, `integrity/binding-matrix.json`, `integrity/rule-corpus.json`.
3. Count ADRs (numbered files in `adrs/`). Note which are Accepted vs Parked.
4. Locate the binding matrix (`integrity/binding-matrix.json` + `tools/audit-binding-matrix.py`). Record total rules, bound count, unbound count, and the percentage.

## Phase 1 — Roof consistency

Check that the consumer-facing door matches the ratified roof (ADR 0011: product = NLC, BBP = emit under the roof, BBA = under-covers integrity).

- [ ] `CHARTER.md` H1 / §3 Practice name — does it open as NLC or as BBP?
- [ ] `DESCRIBE.md` title/opening — NLC-first?
- [ ] `docs/TERMS.md` — does it call CHARTER a "living BBP spec"?
- [ ] README / GETTING-STARTED — NLC hero, no BBA/BBP roof leakage?
- [ ] Path residue: `docs/nlc/compiler/` still present? `bbp-*` nouns exposed in consumer docs?
- [ ] `MANIFESTO.md` / docs manifesto — six principles + layer stack present?

Record each mismatch as a finding: severity, file, evidence, remediation.

## Phase 2 — Gap tracker SSOT

- [ ] Does `FINDINGS.md` claim to be the single SSOT for undone work?
- [ ] Do `HOLES.md`, root `TODO`, and `USE-CASES.md` still coexist as live trackers?
- [ ] Is FINDINGS "Last pass" SHA current vs HEAD?
- [ ] Are any FINDINGS rows stale (claiming a fix that already landed)?

Record each as a finding.

## Phase 3 — Binding matrix completeness

- [ ] Total charter rules vs bound rules. Compute percentage.
- [ ] Classify every unbound rule into one of three buckets:
  - **Structural** (AST/import-graph checkable) — these should have a binder; missing binder = actionable gap.
  - **Semantic** (judgment) — human-gated confirmer, not a static check.
  - **Process** (ratification, ship, signatures) — human-gated by design (C24).
- [ ] Flag any structural rule that is unbound but gateable.

## Phase 4 — Ratification coverage (per-rule ADRs)

- [ ] List every ratification named in document control.
- [ ] For each charter rule, check whether an ADR records the decision, rationale, and alternatives.
- [ ] Rules with no ADR = ratification gap. Count them (decision coverage ≠ gate coverage).
- [ ] Confirm decision-first (ADR) then rule (if-then), per ADR 0007.

## Phase 5 — Soft-green honesty

- [ ] Is "compile ≠ ship" loud and protected (release-audit refuses agent-as-releaser)?
- [ ] Is "Accepted ADR ≠ wired gate" visible (badges on parked items)?
- [ ] Is multi-language fitness language honest (Python-first, others adapter-parked)?
- [ ] Any place where documentation overclaims what the gates actually enforce?

## Phase 6 — Completeness (product gaps)

Cross-check FINDINGS "Needed" and "Parked" rows. For each, confirm it is still accurate or update with evidence. Do not silently close a Needed row.

Also confirm manifesto beliefs bind to ADR 0025 / gates, or file unbound-text findings.

## Output format

Produce a report with these sections, in order:

1. **Audit metadata** — SHA, date, agent, model.
2. **Coverage summary** — ADR count, binding matrix (X of Y bound, Z%), ratification coverage.
3. **Findings** — each: ID (A1, A2…), severity (P0/P1/P2/P3), category, evidence, why it matters, remediation.
4. **Bucket split** — unbound rules three-bucket classification with counts.
5. **Comparison** — if prior list provided: new / resolved / unchanged.
6. **Soft-green residuals** — what this audit does not claim.

## Hard rules

- Cite file paths and sections for every finding. No vague claims.
- Do not implement fixes in the same turn. Audit only.
- Do not reopen the public roof choice (NLC stays NLC).
- Record the exact SHA. If you cannot reach the repo, say so and stop.
- If a phase has no findings, say "no findings" explicitly — do not skip the phase.

## Reference

- Charter: `CHARTER.md`
- Terms: `docs/TERMS.md`
- Findings SSOT: `FINDINGS.md`
- Binding matrix: `integrity/binding-matrix.json`
- ADRs: `adrs/`
- Manifesto: `MANIFESTO.md`, `docs/nlc/compiler/MANIFESTO.md`
- Harness: `docs/nlc/HARNESS.md`
- Human judgment gates: `docs/nlc/HUMAN-JUDGMENT-GATES.md`
