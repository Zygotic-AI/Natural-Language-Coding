# RCA: Planit handoff violated ADR 0038 after shipping full-nlc-audit

**Date:** 2026-09-23  
**Context:** Natural-Language-Coding hub  
**Status:** mitigated (26-09-23 — handoff instruction, manifest/drift fitness, RELEASE + `./release` full profile)

---

## 1. Error condition

**Evidence (observed):**

- After implementing `tools/full-nlc-audit.py`, manifest, and `.agents/skills/full-nlc-audit/SKILL.md`, the agent emitted a **Planit Phase 7 handoff** in chat that:
  - Copied the manifest stage list (“Quick includes: binding matrix, …”) instead of pointing only at `integrity/full-nlc-audit-manifest.json`.
  - Used deictic wording (“Run machine command **above**”).
  - Directed “Follow skill Step I” without naming `.agents/skills/full-nlc-audit/SKILL.md` or `references/inference-phases.md`.
  - Gave inference apex **Continuity: PASS | FAIL** without requiring `FULL_NLC_AUDIT:MET` and exit code in the same handoff block.
- User requested an ADR 0038 violation inventory; semantic review found **9 handoff issues (H1–H9)** and **3 durable-doc issues (D1–D3)**. `python3 tools/fitness-adr-0038-no-memory.py` → **RESULT:MET** (no literal “remember” / “don’t forget” strings in scanned SSOT).

**Mechanism confirmed:** yes — handoff text and [`docs/nlc/FULL-NLC-AUDIT.md`](../docs/nlc/FULL-NLC-AUDIT.md) § Manifest reproduce duplicated inventory (D1) without running new code.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Chat Planit handoff | Second SSOT for stage list + session ritual |
| 4 | [`docs/nlc/FULL-NLC-AUDIT.md`](../docs/nlc/FULL-NLC-AUDIT.md) | Duplicated manifest summary (D1, D2) |
| 3 | Agent Phase 7 habit | Summarize for readability instead of link-only handoff |
| 2 | Planit skill Phase 7 | No ADR 0038 checklist on **chat** handoffs (only §2 gate on durable artifacts) |
| 1 | **ADR 0038 v1 binder scope** | [`tools/fitness-adr-0038-no-memory.py`](../tools/fitness-adr-0038-no-memory.py) scans skills/adoption/`AGENTS.md` only — not `docs/nlc/*`, not agent chat; no rule forbidding manifest duplication in operator docs |

**Furthest controllable upstream point:** **No required Planit Phase 7 handoff profile** (durable instruction + optional fitness) that forces link-only machine procedure and dual apex evidence — so agents default to tribal summaries even immediately after authoring ADR 0038 tooling.

---

## 3. Impact / scope

- Operators or agents may run wrong profile, skip Step M, or trust stale stage lists in chat.
- Irony risk: continuity audit entrypoint introduced via process that violates continuity of SSOT (manifest vs prose).
- v1 ADR 0038 fitness green while semantic 0038 fails — false confidence.

---

## 4. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** Hub must ship a **binding Planit Phase 7 handoff instruction** (`.agents/instructions/planit-phase7-handoff-adr-0038.md` linked from `AGENTS.md` and Planit) that **forbids** duplicated machine inventories and deictic references and **requires** full commands + skill paths + machine pass tokens — and **CI or full-nlc-audit** must fail when `docs/nlc/FULL-NLC-AUDIT.md` (and similar operator docs) enumerate manifest stage ids instead of pointing at the manifest file.

---

## 5. Prevention test

> If **`.agents/instructions/planit-phase7-handoff-adr-0038.md` were linked from Planit Phase 7 and `fitness-full-nlc-audit-manifest-drift.py` (or equivalent) failed when operator docs list stage names not sourced from `integrity/full-nlc-audit-manifest.json`**, the agent could not have shipped the duplicate “Quick includes” handoff and D1 manifest paragraph without the same change failing CI before merge.

---

## 6. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | ADR 0038 handoff pack (TODO table H1–H9, D1–D3) |
| Owner | Hub maintainers |
| Path / artifact | `.agents/instructions/planit-phase7-handoff-adr-0038.md`, `docs/nlc/FULL-NLC-AUDIT.md`, Planit Phase 7, optional `tools/fitness-full-nlc-audit-manifest-drift.py` |
| Verification | `python3 tools/fitness-adr-0038-no-memory.py` → MET; `python3 tools/fitness-full-nlc-audit-manifest.py` → MET; `python3 tools/fitness-full-nlc-audit-manifest-drift.py` → MET; `python3 tools/full-nlc-audit.py --check --profile quick` → MET; `python3 tools/ci_fitness.py` → CI:MET; handoff in `AGENTS.md` + Planit Phase 7 |

---

## 7. repo_touch (ADR 0025)

| Layer | Citation |
| ----- | -------- |
| Belief | Manifesto: process defects, not operator memory |
| ADR | [0038-no-memory-in-process.md](../adrs/0038-no-memory-in-process.md) §1, §3 |
| Rule | [rules/nlc-0038.json](../rules/nlc-0038.json) NLC-0038-01 (v1 literal scan — insufficient alone) |
| Gate | Expand: handoff instruction + manifest-drift fitness (TODO H9, H1) |

---

## 8. Contributing factors

- Planit Done signals emphasize durable artifact gates, not chat handoff shape.
- Successful delivery of `full-nlc-audit` machine path reduced scrutiny on Phase 7 prose.
- No adversarial pass on the handoff block in the same turn (Planit Phase 6 not applied to chat-only deliverable).

---

## Chat summary

- **Error:** Readable Planit summary duplicated manifest and session steps; ADR 0038 §1/§3 violated while v1 regex fitness passed.
- **One thing:** Binding Phase 7 handoff instruction + manifest-drift fitness for operator docs.
- **Next:** Execute TODO rows under “ADR 0038 remediations (handoff + doc drift)”.
