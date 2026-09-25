# RCA: Release PR fitness failed while local `/release` gates passed

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub (`/release`, `./release`, PR #54)  
**Status:** prevented (fetch-depth on `main`; ADR 0039 binder enforces; tag gate shares shipped baseline)

---

## 1. Error condition

**Evidence (observed):**

- Signal: GitHub Actions **fitness** on PR **#54** (`release/v0.2.0` → `main`), run `36189874417`.
- Exit code: job **FAILURE**; `CI:FAIL tools/assert-release-tag-gate-fails.py`.
- Log excerpt: `ASSERT:FAIL expected hub-release-record blocker` immediately before the assert name (landmine did not see `hub-release-record` in tag-gate stderr).
- Reproduction (CI-shaped): `actions/checkout@v4` with default **fetch-depth 1** on PRs → `python3 tools/nlc_release_tag_gate.py --check --commit 397b1a0 --tag v0.2.0 --skip-verify-deep` exits 1 with **“no nlc-version.json at commit”** (commit absent from shallow clone), **not** the `missing integrity/hub-release-record.json` line the landmine expects.
- Reproduction (full history): same assert → **ASSERT:PASS** locally; release branch **did** contain valid `integrity/hub-release-record.json` on commit `cdb3826`.

**Inferred (label clearly):**

- Operator read the assert message as “PR missing hub-release-record”; the PR was fine—the **landmine’s pinned SHA was unreachable in CI**.

**Mechanism confirmed on reproduction:** yes — shallow vs full clone changes tag-gate stderr; CI log + local `gh run view` + landmine source `BAD_COMMIT = "397b1a0"`.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | PR #54 fitness | Landmine false FAIL; release blocked after push |
| `./release` push leg | `scripts/nlc-release.sh` | Pushed `release/v0.2.0` after local `verify-deep` / prep; **no check** that **Actions checkout** can run git-SHA landmines |
| Agent `/release` | `.agents/skills/release/SKILL.md` | Ran `ci_fitness.py` on **full local clone** → **CI:MET**; did not model **PR workflow checkout depth** |
| ADR 0039 binder | `fitness-adr-0039-release-binder.py` | Wired tag gate, record, `release.yml`; **did not** bind `.github/workflows/fitness.yml` to landmine git history needs |
| Landmine | `assert_release_tag_gate_fails.py` | Assumes historic merge `397b1a0` exists in clone when asserting NOT_MET text |
| Workflow | `.github/workflows/fitness.yml` | Default shallow checkout on PRs until `fetch-depth: 0` fix (`e313a8a`) |

**Furthest controllable upstream point:** **Release binder / ship contract** — treat “PR fitness green” as part of releasability, including **workflow checkout compatible with release landmines**, not only `./release` steps on a developer machine.

---

## 3. Impact / scope

- Hub **0.2.0** ship delayed; operator debug time on misleading “hub-release-record” wording.
- Trust hit: **`/release` said MET locally** while **release PR CI failed** for an environmental mismatch `./release` never validated.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-25 | `./release --bump keep`; `release/v0.2.0` pushed; PR opened |
| 26-09-25 | Fitness CI FAIL on landmine assert |
| 26-09-25 | `fetch-depth: 0` added on release branch (`e313a8a`); assert passes locally |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer (one sentence):** **Extend the ADR 0039 release fitness binder so `.github/workflows/fitness.yml` must use `fetch-depth: 0` whenever release tag-gate landmines pin a historic git SHA—so `./release` / hub CI cannot ship a release PR workflow that false-fails landmines.**

---

## 6. Prevention test

> If **`fitness-adr-0039-release-binder.py` enforced fetch-depth: 0 on fitness.yml when BAD_COMMIT landmines exist`** had been in place **before** the failure, **PR #54 fitness could not have failed with ASSERT:FAIL expected hub-release-record blocker due to a shallow clone**, because **the workflow would have been rejected at hub CI bind time until checkout depth matched landmine requirements**.

**Completed:** See §8 verification.

---

## 7. Contributing factors (optional)

- Misleading assert string when tag gate fails early (missing commit vs missing record).
- `./release` branch UX (separate RCA-worthy: double confirm default **N** on `main`).
- Landmine uses **mistaken historic** `397b1a0` tag commit—valid for gate semantics but increases clone-depth sensitivity.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Require `fetch-depth: 0` in `fitness.yml` via ADR 0039 release binder when `assert_release_tag_gate_fails` pins `BAD_COMMIT` |
| Owner | Hub maintainers |
| Path / artifact | `tools/nouns/fitness_adr_0039_release_binder/fitness_adr_0039_release_binder.py`, `.github/workflows/fitness.yml` |
| Verification | `python3 tools/fitness-adr-0039-release-binder.py` → RESULT:MET; regress by removing `fetch-depth: 0` → VIOLATION |
| Human acceptance | `accepted` (planit remediate 26-09-25) |
| Implementation route | Landed on `main`: binder + `resolve_shipped_*` in tag gate |

---

## 9. Follow-up (detection only if prevention insufficient)

- Optional: `./release` pre-push echo if `fitness-adr-0039-release-binder` NOT_MET (human-readable, not a second quiz).
- Optional: tag-gate early exit mentions “commit not in clone (shallow checkout?)” when `git show` fails.
