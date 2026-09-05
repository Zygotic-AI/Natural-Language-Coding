# PR-004 Delta Notes

## Delta 1 — 2026-09-05

**Finding:** F1 (blocking) — Binding matrix S7/CS7 pointed at `integrity/audits/A-S7.md` and `integrity/audits/A-CS7.md` but files were missing.

**Fix:** Added `integrity/audits/A-S7.md` and `integrity/audits/A-CS7.md` matching the S1–S6 / CS1–CS6 audit-def pattern.

**Files added:**
- `integrity/audits/A-S7.md` — Audit definition for S7 (produce→fitness handoff default-closed)
- `integrity/audits/A-CS7.md` — Audit definition for CS7 (package present before fitness; refuse≠FAIL)

**Verification:** `verify.sh` still passes (13/13 checks).

**Status:** Ready for Reed delta fitness then Vera adversarial.
