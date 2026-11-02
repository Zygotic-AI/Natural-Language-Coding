# RCA: `.nlc/before-generate-stamp.json` scopes on PR #43

**Date:** 2026-10-28 (recorded 2026-10-29)  
**Context:** Natural-Language-Coding hub, `release/v0.4.1`, read-only branch `cursor/v041-dogfood-license-rename` (PR #43)  
**Status:** open (RCA only; no remediation in this record)

**Scope (manifest):** Analysis only. New file `docs/rca/2026-10-28-before-generate-stamp-scopes.md`. No tool, check, workflow, goal, or stamp commits.

---

## 1. Error condition

**Observed on PR #43:**

| Commit | Stamp `scopes` | `product_content_sha256` vs tree | Verify symptom |
| ------ | ---------------- | -------------------------------- | -------------- |
| `c05b76b` | `["default"]` only | Matches tree at that commit | Stamp narrowed; gate-set manifest regenerated |
| `ad278a7` | Restored four scopes from `release/v0.4.1` tip | **Mismatch** (stamp still `890a0a0f…`, tree moved) | `pipeline-blockers` NOT_MET |

**Reproduction (writer on `c05b76b` checkout):**

```text
$ rm -f .nlc/before-generate-stamp.json
$ ./nlc maintainer guide before-generate
KNOWLEDGE_DOMAIN scope=default status=empty facts=0
BEFORE_GENERATE:MET
Before-generate passed. Stamp written under .nlc/
$ cat .nlc/before-generate-stamp.json
{
  "ok": true,
  "scopes": [
    "default"
  ],
  ...
}
```

**Reproduction (`pipeline-blockers` on `ad278a7` checkout):**

```text
$ ./nlc gate pipeline-blockers --tree .
FAILED pipeline-blockers on tree .
Reproduce: ./nlc gate pipeline-blockers --tree .
  product changed after before-generate stamp (content fingerprint mismatch) (re-run ./nlc maintainer guide before-generate)
$ echo $?
1
```

---

## 2. Every writer of `.nlc/before-generate-stamp.json`

| Writer | Path | Write site (line) | Role |
| ------ | ---- | ----------------- | ---- |
| Production | `tools/nouns/guide_state/guide_state.py` | `_write_json` at lines 18-19; target path at lines 77-78 | `before_generate_ok()` persists stamp after knowledge gate passes |
| CLI trigger | `tools/nouns/guide_cmd/guide_cmd.py` | line 44 | `run_before_generate()` calls `before_generate_ok(root, scopes)` after `nlc-before-generate.py` exits 0 |
| Landmine fixture | `tools/nouns/assert_goal_write_hook_landmine/assert_goal_write_hook_landmine.py` | lines 106, 157 | Synthetic trees for hook tests |
| Landmine fixture | `tools/nouns/assert_rule_emit_sync_passes/assert_rule_emit_sync_passes.py` | line 27 | Temp workdir for rule-emit landmine |

**Goals:** No goal `execute.sh` writes the hub stamp. `goals/hub_session/execute.sh` line 24 only prints a reminder to run `tools/nlc-before-generate.py`.

**Not writers:** `tools/nlc-before-generate.py` / `tools/nouns/nlc_before_generate/nlc_before_generate.py` validate knowledge only (exit 0/1); they do not open the stamp file for write.

Line numbers verified at `release/v0.4.1` commit `57a7e372a59bd69c03d30545517e5d7aba3268ec`.

---

## 3. How the `scopes` list is computed

1. **CLI parsing:** `tools/nouns/guide_cmd/guide_cmd.py` lines 79-80: `scopes = args.scope or ["default"]` for `./nlc maintainer guide before-generate`.
2. **Knowledge gate (pre-write):** `run_before_generate()` lines 26-29 build argv for `tools/nlc-before-generate.py` with one `--scope` per list entry.
3. **Harness script:** `tools/nouns/nlc_before_generate/nlc_before_generate.py` line 34: `scopes: list[str] = args.scope or ["default"]`; lines 47-64 run `load-knowledge-domain.py` once per scope.
4. **Persisted JSON:** `before_generate_ok()` stores the same list under `"scopes"` (`guide_state.py` lines 77-84). No merge with prior stamp; no hub-specific scope expansion in code.

**PR #43 `c05b76b`:** Commit message "chore: sync hub hash, install fingerprints, and gate-set manifest" includes a stamp diff that drops `release`, `hub_release`, and `sign_adrs`. That shape matches `./nlc maintainer guide before-generate` with **no** `--scope` flags (reproduction above on checkout `c05b76b`).

**Trunk reference (`release/v0.4.1` at `57a7e37`):** `.nlc/before-generate-stamp.json` lists four scopes; those names are only present because an operator passed four `--scope` values when that stamp was last written. Nothing in `load-knowledge-domain.py` or `guide_cmd.py` adds them automatically.

---

## 4. Which check reads the stamp (releasable verify profile)

**Profile SSOT:** `integrity/releasable-gates.json` lines 6-9: profile `verify` includes gate id `pipeline-blockers`.

**Gate wiring:** `tools/nouns/releasable_gates/releasable_gates.py` lines 62-66: `pipeline-blockers` builtin calls `pipeline_blockers(tree)`.

**Blocker chain:** `tools/nouns/verify/verify.py` lines 118-136: `pipeline_blockers()` extends `verify_fast_blockers(root)`.

**Stamp read:** `tools/nouns/compliance/compliance.py` lines 81-108: `before_generate_stamp_blockers()` loads `.nlc/before-generate-stamp.json`, requires `ok`, compares `product_content_sha256` to `product_content_fingerprint(root)`; lines 343-343: `verify_fast_blockers()` calls it.

**Hub verify entry:** `verify.py` lines 148-152: hub repos run `run_profile("verify", root)` after fast fingerprint checks.

**Failure on `ad278a7`:** Restored stamp bytes from an older tree (`890a0a0f…`) while PR branch product bytes differ; `before_generate_stamp_blockers()` line 104-107 fires. Reproduction output in section 1.

---

## 5. Does dropping `release`, `hub_release`, and `sign_adrs` from the stamp JSON weaken any gate?

**Answer: No** for gates that **read** the committed stamp file.

**Evidence:** `before_generate_stamp_blockers()` (`compliance.py` lines 91-108) never reads `"scopes"`. `before_generate_stamp_valid()` (`guide_state.py` lines 88-104) checks `ok` and `at` age only. `ensure_before_generate_stamp()` (`uc_blockers.py` lines 484-497) calls `before_generate_stamp_valid()` only.

**Caveat (UC18 at write time, not a gate read):** Fewer `--scope` flags means fewer `load-knowledge-domain` runs before the stamp is written (`nlc_before_generate.py` lines 47-64). That weakens the **pre-generate knowledge gate**, not a downstream reader of `"scopes"`.

---

## 6. Defective product, process, root

| Layer | What failed | Evidence |
| ----- | ----------- | -------- |
| **Symptom** | Stamp on PR #43 held only `"default"` then a restore commit left a stale fingerprint | `git show c05b76b:.nlc/before-generate-stamp.json`; `ad278a7` gate output |
| **Defective product** | `.nlc/before-generate-stamp.json` committed on a **content** PR as part of hub-hash chore, with default-only scopes and bytes that do not stay valid across subsequent edits on the same branch | `c05b76b` diff vs parent; `ad278a7` mismatch reproduction |
| **Process** | Mechanical sync (hub content hash, install fingerprints, gate-set manifest) treated the stamp as another generated artifact to refresh using the default guide invocation, without hub multi-scope intent or "stamp last after all product edits" | `c05b76b` commit message and file list; writer defaults in `guide_cmd.py` 79-80 |
| **Root (process rule gap)** | No bound rule separates **UC18 harness evidence** (stamp tied to `goals/` / `domain/` fingerprint) from **ordinary PR content**, and no checklist binds **which `--scope` values** hub work must pass before the stamp may change. ADR 0010 gates **generate** paths; it does not forbid committing a partial stamp during unrelated sync chores. Remediation text in `compliance.py` line 101 ("all hub scopes") is operator prose, not machine-enforced scope list. | ADR 0010; `integrity/check-inputs.json` has no row declaring hub root stamp inputs for content PR classes (open since PR #41) |

---

## 7. Should the stamp be in `check-inputs.json`? (open question; not decided)

**Today:** Hub `.nlc/before-generate-stamp.json` appears in `integrity/mandated-paths.json` and in `integrity/gate-set-baseline.manifest.sha256` (signed member). It is **not** listed as a declared input path for `pipeline-blockers` or hub-content freshness in `integrity/check-inputs.json` (only example-tree stamps appear under landmine labels).

**RCA answer for owners:** Listing the stamp in `check-inputs.json` would make fitness declare when stamp bytes are in scope for a change class; it would **not** by itself fix wrong scopes or stale fingerprints. Pair any declaration with scope enumeration or "do not commit on content-only PRs" policy.

---

## 8. Does the stamp belong in a content PR's scope?

**Answer: No** for PR #43-shaped work (license rename, docs, dogfood audit).

**Evidence:** Stamp `product_content_sha256` hashes `goals/` and `domain/` product paths (`compliance.py` `product_content_fingerprint`). PR #43 commits changed other tracked paths first; refreshing the stamp mid-PR without re-running after the last product edit yields `ad278a7` failure. The stamp is also a **signed gate-set member** (`integrity/gate-set-baseline.manifest.sha256` line for `.nlc/before-generate-stamp.json`), so casual stamp commits force manifest regeneration and owner signature work unrelated to license text.

---

## 9. Remediation options (not implemented)

1. **Policy:** Content PRs must not commit `.nlc/before-generate-stamp.json`; stamp updates only on hub harness / release prep PRs with documented `--scope` list.
2. **Machine scope list:** Encode required hub scopes (e.g. `default`, `release`, `hub_release`, `sign_adrs`) in one SSOT JSON; refuse `before_generate_ok` unless argv scopes are a superset.
3. **check-inputs:** Add hub stamp path to inputs for checks that read it; wire `fitness-check-inputs-declaration` so content PRs cannot silently omit stamp coupling.
4. **Gate-set / digest:** Exclude stamp from signed manifest (freshness-only), per Option A in `docs/rca/2026-10-25-signed-whole-tree-digest.md`, so doc PRs do not remanifest for stamp churn.
5. **Operator finish line:** Extend `/release` or planit step 6 checklist: after all edits, `./nlc maintainer guide before-generate` with full hub scopes, then verify profile green, then commit stamp once.

---

## 10. Related references

- ADR 0010 (gate after every generate): `adrs/0010-gate-after-every-generate.md`
- UC18 proof row: `docs/USE-CASES-PROOF.md` (`before_generate_stamp_blockers`)
- Harness doc: `docs/nlc/HARNESS.md` line 10
- Prior stamp + pipeline failure on another release line: `docs/rca/2026-10-25-planit-unregistered-skill-edit.md` timeline row 2026-10-25 00:50:54
