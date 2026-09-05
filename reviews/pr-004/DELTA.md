# PR-004 Delta Notes

## Delta 1 — 2026-09-05

**Finding:** F1 (blocking) — Binding matrix S7/CS7 pointed at `integrity/audits/A-S7.md` and `integrity/audits/A-CS7.md` but files were missing.

**Fix:** Added `integrity/audits/A-S7.md` and `integrity/audits/A-CS7.md` matching the S1–S6 / CS1–CS6 audit-def pattern.

**Files added:**
- `integrity/audits/A-S7.md` — Audit definition for S7 (produce→fitness handoff default-closed)
- `integrity/audits/A-CS7.md` — Audit definition for CS7 (package present before fitness; refuse≠FAIL)

**Verification:** `verify.sh` still passes (13/13 checks).

---

## Delta 2 — 2026-09-05

**Findings:** Vera adversarial A1/A2 (R20, S7, S3, ADR 0004)

### A1 — handoff_token required vs optional drift

**Issue:** `standards-steward/verbs.md` note implied token required; `quality-architect/verbs.md` and `BOUNDARY-IO.md` treated it optional. Contract surfaces disagreed (R20).

**Resolution:** Token optional everywhere. Hard gate = package completeness (S7), not token presence.

**Files updated:**
- `agents/standards-steward/verbs.md` — Note replaced: token is convenience; hard gate is package completeness
- `agents/quality-architect/verbs.md` — handoff_token optional; if present must match issuance
- `reviews/pr-004/BOUNDARY-IO.md` — handoff_token optional; hard gate note added
- `reviews/pr-004/ADVERSARIAL.md` — Hole 2 marked RESOLVED (optional end-to-end; package is hard gate)

### A2 — standards-steward completion artifact missing produce package

**Issue:** `standards-steward/AGENT.md` completion artifact said "proposal ready for review" without produce package / `complete-produce` (S3, S7, ADR 0004).

**Resolution:** Updated completion artifact to include produce package row; completion for fitness handoff = change + package + complete-produce complete; added Produce verbs section listing `complete-produce`.

**Files updated:**
- `agents/standards-steward/AGENT.md` — Completion artifact table + handoff-out + produce verbs

**Verification:** `verify.sh` still passes; `rg "requires the token" agents/standards-steward/verbs.md` empty.

**Status:** Ready for Reed delta fitness → Vera adversarial.
