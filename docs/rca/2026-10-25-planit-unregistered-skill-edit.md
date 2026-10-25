# RCA: Unregistered Planit skill edit landed on `release/v0.4.0` with no PR

**Date:** 2026-10-25  
**Context:** Natural-Language-Coding hub — 0.4.0 prepare line  
**Status:** open (RCA only; no remediation in this record)

**Scope (user words):**

- “RCA ONLY. Do NOT change any code, skills, registries, manifests, or branches.”
- “Incident: commit d4b4648 … was pushed directly to release/v0.4.0 with no PR.”
- “It edited `.agents/skills/planit/SKILL.md` … but `integrity/planit-skill-registry.json` still says 85a11ef6….”
- “`python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md` gives `PLANIT_IDENTITY:NOT_MET`, and the owner's local hook now denies work.”
- “Next, da90b90 regenerated the gate-set manifest, which is now unsigned.”
- “first name the defective product, then the process that produced it, and climb until you reach a root that, if fixed, would have prevented this whole class.”
- “How could this condition be created where we made a mandate for a signature and still allowed the skill edits to treat it as optional? What created that condition?”
- “Climb one level above the current root: find what CREATED the condition that signature/identity pins are optional later steps for skill produce.”
- “RCA ONLY, no remediation changes.”

---

## 1. Error condition

**Observed (bounded, reproducible):**

- `origin/release/v0.4.0` tip is `da90b909cb6470d8b2ff97b85778016985a63efc` (parent `d4b46487fe7319d209c9366d829f81ca3716d73c`). Neither commit is a merge. GitHub `GET /commits/{sha}/pulls` returns `[]` for both.
- `d4b4648` (Cursor Agent, 2026-10-25 00:50:16 UTC): “Repair published skills so the live author check is MET.” Touches 30 files, including `.agents/skills/planit/SKILL.md` and ten other published `SKILL.md` files. Does **not** touch `integrity/planit-skill-registry.json` or `integrity/nlc-install-hashes.json`.
- Current Planit bytes: `sha256 0e0493b4c0c95e56c53501d1a4d794ed7b699cc9cc5ad715c92709626f845d9f` (`.agents/skills/planit/SKILL.md`). Parent `ae6dcb6` of the repair still hashed `85a11ef6ce5037d3a4e0c54d074679598a19e347f4e1f80778d4f2f1ad15085e`.
- Registry still records that parent hash (`integrity/planit-skill-registry.json` line 4).
- Reproduction (this tree): `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md` → `VIOLATION loaded Planit skill hash does not match the registry` / `PLANIT_IDENTITY:NOT_MET` (exit 1).
- Cursor hook `.cursor/hooks/nlc-planit-identity.sh` (wired on `beforeSubmitPrompt` in `.cursor/hooks.json`) denies the prompt when that command is non-zero. That is the owner-local deny.
- `da90b90` (00:50:51 UTC): “Regenerate the unsigned gate-set manifest after the skill repair.” Only `integrity/gate-set-baseline.manifest.sha256` changes. `python3 tools/fitness-gate-set-manifest.py` → `VIOLATION … Content-SHA256 mismatch (statement 8ffa1481… vs file 1f3a82e5…)` / `RESULT:NOT_MET`.

**Not the error condition:** the YAML `name:` / in-skill-link repair itself. `python3 tools/nlc-skill-author-check.py --root .agents/skills` is `SKILL_AUTHOR:MET` after `d4b4648`. That is the gate the produce ran.

---

## 2. Defective product, then the process (climb)

| Layer | What it is | Evidence |
| ----- | ---------- | -------- |
| **(symptom) product** | Planit skill bytes on `release/v0.4.0` no longer match the identity pin; install fingerprints for nine published skills are stale; gate-set sidecar is unsigned | `PLANIT_IDENTITY:NOT_MET`; `INSTALL_VERIFY:NOT_MET` (nine paths); `fitness-gate-set-manifest` Content-SHA256 mismatch |
| **5. Landing** | Those commits updated `origin/release/v0.4.0` with no PR | `git cat-file -p d4b4648` has one parent; GitHub pulls API `[]`; branch `protected: false` |
| **4. Produce session** | Cloud run `bc-298e948a-5bf8-520b-84f0-5adf8e09ff99` executed walkthrough step 5, proved `SKILL_AUTHOR:MET`, pushed the release line, then regenerated an unsigned manifest | Transcript (00:50 UTC); commit messages; handoff: “did not bump identity” |
| **3. Walkthrough / type recipe** | Step 5’s machine finish line is the author checklist only. Skill type recipe has no identity or install-hash pin. “Refresh Planit identity if `planit/SKILL.md` bytes change” was unbound prose | Transcript step list; `content-types/HOW-TO-ADD.md` Skill section; ADR 0054 |
| **2. Pin design** | Identity registry is a hand-kept pin (ADR 0046) with no generator. Install hashes and gate-set manifests **are** generated, but Skill produce does not require those generators. Identity hook fires on local prompt-submit, not on commit/push | `integrity/planit-skill-registry.json`; `tools/nlc-install-hash-update.py`; `tools/generate-gate-set-baseline-manifest.py`; `.cursor/hooks.json` |
| **1. Host + brief** | `release/v*` is the working ship line (ADR 0044). GitHub has no ruleset and no protection on that branch. `RELEASE.md` recommends PR+CI only for `main`. Cloud briefing says “create a feature branch + PR”; `/release` and the walkthrough say commit on `release/v*` and defer the one PR to `./release` | Branch API; `docs/adoption/RELEASE.md`; `.agents/skills/release/SKILL.md`; transcript 256229 |

**Furthest controllable upstream point:** published-skill **produce** is not an atomic pin update, and the release line will accept a partial produce. Fixing only the current `SKILL.md` hash, or only the hook message, recreates the class the next time a walkthrough names one checklist as done.

---

## 3. Impact / scope

- Owner-local Planit intake is denied (`beforeSubmitPrompt` fail-closed) on any checkout of this tip.
- Hub `verify` profile is red: `planit-skill-identity` failed on both `d4b4648` and `da90b90` (GitHub Actions fitness runs `40148249783` and `40148286806`).
- Piped install on the same runs is `INSTALL_VERIFY:NOT_MET` (fingerprint list) / skill-author import failure on Windows (missing `yaml`) — separate contributing failure.
- Gate-set member bytes were regenerated without owner ratification. The produce named that as expected until a later sign step.
- `release/v0.4.0` is the 0.4.0 prepare line. These commits are on the line that `./release` would offer as the ship PR to `main`.

---

## 4. Timeline (brief)

| Time (UTC) | Event |
| ---------- | ----- |
| 2026-09-16 | ADR 0010 accepted: never pass generated output downstream before its gate |
| 2026-10-08 | ADR 0046: `integrity/planit-skill-registry.json` pins Planit path + SHA-256; Cursor hook on prompt-submit |
| 2026-10-11 | Registry last content change in history: `5bd6113` (O6). No generator exists |
| 2026-10-20 | RCA: skill YAML load errors. Repair of live skills is a later tracked row |
| 2026-10-20 | PR #26 (draft, base `main`): “Does **not** rewrite current hub skills (repair is a tracked TODO)” |
| 2026-10-24 19:38–00:46 | Direct pushes to `release/v0.4.0` (no PR from `ca001b9` onward). Fitness already failing on this line |
| 2026-10-24 ~session | Operator: “List the steps…”; agent emits 10-step 0.4.0 walkthrough. Step 5 = repair + “Refresh Planit identity if `planit/SKILL.md` bytes change.” Step 8 = owner sidecar last. Step 10 = one PR via `./release` |
| 2026-10-24 | Operator: “Let's walk through each one… Let's start now” |
| 2026-10-25 00:49 | Operator: “ok, what's next, go ahead and do it.” Agent maps that to step 5 |
| 2026-10-25 00:50:16 | `d4b4648` on `release/v0.4.0`; push `git push -u origin release/v0.4.0` (no PR). TODO row `@done(26-10-24 19:49)` |
| 2026-10-25 00:50:21 | Fitness workflow `40148249783` starts **after** the push; `FAILED planit-skill-identity` / `PLANIT_IDENTITY:NOT_MET` |
| 2026-10-25 00:50:51 | `da90b90` unsigned manifest regenerate; second push |
| 2026-10-25 00:50:54 | Fitness `40148286806`: same identity fail + pipeline-blockers (before-generate stamp) |

---

## 5. Mechanism on reproduction

**Confirmed (product):** parent Planit hash `85a11ef6…` equals the registry; tip Planit hash `0e0493b4…` does not. `prove()` in `tools/nouns/planit_identity/planit_identity.py` compares loaded bytes to `content_sha256` and returns the violation used by the hook and by `planit-skill-identity`.

**Confirmed (CI after land):** fitness.yml `on: push` ran `bash tools/ci-fitness.sh` → `ci_fitness.py` `main()` with `include_releasable_verify=True`. Verify profile includes `planit-skill-identity`. Both incident SHAs failed that gate in <10s. The job cannot refuse a push that already succeeded.

**Confirmed (process):** transcript of `bc-298e948a` at 00:50 UTC: agent notes no PR exists, walkthrough defers the ship PR to `./release`, cloud briefing wants a PR, walkthrough wins; `git push origin release/v0.4.0`. Handoff: “did not bump identity… Regenerated the unsigned gate-set… owner ratification stays the later sign step.” Verified list is `SKILL_AUTHOR:MET` plus author-checklist fitness; identity is absent.

**Confirmed (host):** `GET /repos/Zygotic-AI/Natural-Language-Coding/branches/release/v0.4.0` → `"protected": false`, `"protection": {"enabled": false, "required_status_checks": {"enforcement_level": "off", "contexts": [], "checks": []}}`. `GET …/rulesets` → `[]`. Detailed `…/protection` and org rulesets return 403 to this integration; the branch object is enough to show this ref is not protected.

---

## 6. The five questions

### Q1. Why could an agent push straight to `release/v0.4.0` with no PR?

**Host:** GitHub does not protect that ref. Repo rulesets are empty. Required status checks are off. A fast-forward `git push origin release/v0.4.0` is accepted. Contrast: `docs/adoption/RELEASE.md` lines 71–74 recommend PR + required CI **for `main` only**, and do not require a PR to update `release/v*`.

**Brief (hub):** ADR 0044 decision 1: unreleased work lives on `release/v*`. `/release` skill lines 64 and 74: prepare commits go on the release line branch, never `main`; the one PR is `release/v*` → `main` via `./release`. The 0.4.0 walkthrough step 2 restated that: “Feature branches aimed at `main` are not the ship.”

**Brief (cloud harness):** this class of run is also told to create a feature branch and open a PR per branch. The producing session recorded the conflict and chose the hub walkthrough (`transcript.json` thinking at the first push: “Cloud instructions suggest creating a PR instead. The user's locked walkthrough takes priority.”).

**Pattern:** from `ca001b9` through `da90b90`, GitHub `commits/{sha}/pulls` is `0`. Direct push to the release line is the in-force landing path, not a one-off.

### Q2. Why did no check run **before** that push catch the registry mismatch?

| Check | When it runs | Did it catch this? |
| ----- | ------------- | ------------------ |
| `.cursor/hooks/nlc-planit-identity.sh` | Cursor `beforeSubmitPrompt` on a local checkout | After the fact, on the owner's machine. Not installed as a git hook. Cloud commit/push does not run it |
| Repo git hooks | `pre-commit` / `pre-push` | Only `*.sample` files under `.git/hooks`. `core.hooksPath` is the cloud agent-hooks dir, not a repo fitness path. No pre-push identity check ran |
| `planit-skill-identity` in releasable verify | First block of `python3 tools/ci_fitness.py` (`include_releasable_verify=True`, `integrity/releasable-gates.json` lines 6–8 and 80–92) | **Yes, after the push.** Run `40148249783` job `fitness` at 00:50:26 UTC: `FAILED planit-skill-identity` / `PLANIT_IDENTITY:NOT_MET` / `CI:FAIL releasable verify profile`. Same on `da90b90` |
| `fitness.yml` `on: push` | After GitHub accepts the ref update | Ran; failed; could not un-land the commits because the branch does not require the check |
| Skill author check | What the produce actually ran | `SKILL_AUTHOR:MET` — different pin |

The check that should have caught the mismatch is `planit-skill-identity` (ADR 0046 binder in `integrity/adr-gates.json` line 185). It ran in CI and is the same command as the owner hook. It is not a pre-push gate. Fitness on this line was already failing before `d4b4648` (runs on `ca001b9`, `bcb2f95`, `4f3caf2`, `15c9bb0`, `ae6dcb6`), so a red status check was not treated as a stop.

### Q3. Why does editing a skill not require or produce a registry update? Derived or hand-kept?

**Three pins, three update stories:**

| Pin | Kind | Updater | Bound to Skill type? |
| --- | ---- | ------- | -------------------- |
| `integrity/planit-skill-registry.json` | Hand-kept identity pin (path + `content_sha256`) | **None.** Last history change `5bd6113`. ADR 0046 stores the hash; nothing regenerates it | No. Skill recipe gate is only `frontmatter-yaml` + `in-skill-links` (`content-types/HOW-TO-ADD.md` lines 296–328; ADR 0054 decisions 1–3) |
| `integrity/nlc-install-hashes.json` | Derived install fingerprint list (includes every `.agents/skills/**/SKILL.md`) | `python3 tools/nlc-install-hash-update.py` (`tools/nouns/install_hash_update/install_hash_update.py` lines 55–57 walk `SKILL.md`) | No. Repair did not run it |
| `integrity/gate-set-baseline.manifest.sha256` | Derived member digest list; ratification is the OpenPGP sidecar | `python3 tools/generate-gate-set-baseline-manifest.py` (header: “no ratification”) | Partial: the session **did** regenerate members (`da90b90`) and **explicitly** left the sidecar unsigned until walkthrough step 8 |

The identity registry is **hand-kept**. It is not a derived artifact today. The install-hash file **is** derived and should have been regenerated in the same change; the Skill type does not say so. Editing a skill to pass `SKILL_AUTHOR` is a complete Skill-type produce. ADR 0046 identity is a **load-time** refuse for Planit intake, not a **produce-time** refuse on `SKILL.md` writes.

### Q4. Who asked for the repair, and was it under an owner-approved plan?

**Asked by the operator**, inside a locked 0.4.0 walkthrough, not by a new `/planit` at repair time.

| Layer | Wording | Where |
| ----- | ------- | ----- |
| Program | Bind the checklist as law; use Planit for the plan; repair is a tracked TODO, not prompt-only law | Transcript `bc-298e948a` (user, earlier in the same run); PR #26 body: “Does **not** rewrite current hub skills (repair is a tracked TODO)” |
| Plan | Walkthrough step 5: repair so `SKILL_AUTHOR:MET`; also “Refresh Planit identity if `planit/SKILL.md` bytes change” | Transcript assistant text listing steps 1–10 |
| Lock | “Let's walk through each one. You guide. … Let's start now” | Transcript user |
| Execute | “ok, what's next, go ahead and do it” | Transcript user, immediately before step 5 |
| Record | TODO: “Repair current published skills so … `SKILL_AUTHOR:MET`” `@done(26-10-24 19:49)` | `TODO` line 678, committed in `d4b4648` |
| RCA follow-up | 2026-10-20 record updated in the same commit to say live skills were repaired | `docs/rca/2026-10-20-skill-yaml-terms-link-load-error.md` in `d4b4648` |

**Owner-approved:** executing the repair so the live author check is MET, on the 0.4.0 line, yes — that is the TODO + walkthrough step 5 + “go ahead.”  
**Not approved as a complete produce:** landing unregistered bytes. Step 5’s own prose required a Planit identity refresh when those bytes changed. The session treated `SKILL_AUTHOR:MET` as sufficient and wrote “did not bump identity.” No GitHub issue asked for a no-PR push. No PR on this branch reviewed `d4b4648`.

ADR 0025: this is not “the agent skipped a sentence.” The Skill type and ADR 0054 make `SKILL_AUTHOR` the only bound gate for that edit, so unbound prose (“refresh identity”) cannot refuse the handoff.

### Q5. Full list of files whose registered hash no longer matches

Derived with repo tools on this tip (`da90b90`), not guessed.

**A. Identity pin** — `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md`

| File | Registered (`planit-skill-registry.json`) | Actual |
| ---- | ----------------------------------------- | ------ |
| `.agents/skills/planit/SKILL.md` | `85a11ef6ce5037d3a4e0c54d074679598a19e347f4e1f80778d4f2f1ad15085e` | `0e0493b4c0c95e56c53501d1a4d794ed7b699cc9cc5ad715c92709626f845d9f` |

`.cursor/skills` is a symlink to `../.agents/skills` (same bytes, not a second registered path).

**B. Install fingerprints** — `python3 tools/nlc-install-verify.py` → `INSTALL_VERIFY:NOT_MET` (nine mismatches). Registered values from `integrity/nlc-install-hashes.json`:

| File | Registered | Actual |
| ---- | ---------- | ------ |
| `.agents/skills/bbp-confirmer/SKILL.md` | `4cf9a5009d5a92e9425ac9e4e987c243e85625e728e8419efd3005224a179ef4` | `6ed5bc11a3e3475d6d626f35259331251ad199152afdb8d598c66c3c9a1c8554` |
| `.agents/skills/bbp-proposer/SKILL.md` | `f3f9d588e7801fab70987c4b3afcbba19f52ea91efb6e173b5ffd2edee333352` | `4c2d40a2cbc33365c75680630920beb3d1afea321e6b13c6e408514e7539d029` |
| `.agents/skills/bbp-recorder/SKILL.md` | `7ee8659d50003bfe3f421ec1bd77b85f34cf2d3cae48a0ae5d753a5d27c79bb4` | `87f5ea131682e03eee71f706111ad24521cfab0db6946b0920a40d782b0330e1` |
| `.agents/skills/bbp-reviewer/SKILL.md` | `7c0c3e265bc52d28e3fea9a8fb02a735bf75cf17fb58ba42fcc414b47225ea5a` | `24ed5101dfdec2080d6a789aa533af17eaca1937e8066e24ad05725ac7db1655` |
| `.agents/skills/full-nlc-audit/SKILL.md` | `ad3f63966d69e7b4609a5370f62ac28210f6b8881ac3c444d2c04b23f63fcefc` | `5dcd8e90f2e08eec8493a705e5ccf02cd4f1a1a528c411f2a5d89c4c45a03866` |
| `.agents/skills/interview/SKILL.md` | `1d7a8861e476d1220bcb1144985a77266a7b914d6688a7c9ade59f97e0496e58` | `73ea432dc2492048e9df5835aab98ca5785a6cd961cb96d61765695df492c403` |
| `.agents/skills/planit/SKILL.md` | `85a11ef6ce5037d3a4e0c54d074679598a19e347f4e1f80778d4f2f1ad15085e` | `0e0493b4c0c95e56c53501d1a4d794ed7b699cc9cc5ad715c92709626f845d9f` |
| `.agents/skills/release/SKILL.md` | `a83161f30b2d6e37f21e7a8ac02f25fde8ec349b491e98621d415b5e2db03331` | `da71736d62912baee10bf3d068e0b26c494435d2418fffa83e55e2708fe72662` |
| `.agents/skills/verify/SKILL.md` | `70b0604fef757f4194892288cec4acdf00b91cd30ffc2b4f048388c7b1a73831` | `4164ff20b6966bb08a5d0f5385092d90abdc36e5498d77b92001a58cf4a52fee` |

Still matching in that manifest (not edited in `d4b4648`): `.agents/skills/nlc-hub-audit/SKILL.md`, `.agents/skills/requirement-pack-ingest/SKILL.md`.

**C. Gate-set sidecar (not a skill-file hash):** member lines were rewritten to the current tree in `da90b90`. The **signed statement** still names Content-SHA256 `8ffa1481…` vs file `1f3a82e5…`. That is an unsigned regenerate, not a ninth skill mismatch.

---

## 7. Candidate roots (at most three)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Update `planit-skill-registry.json` (and install hashes) to `0e0493b4…` | Output-only; next skill repair repeats | Reject |
| Add a pre-push script | Detection; cloud/agent-hooks can skip repo hooks; unsigned gate-set and no-PR landing remain | Too low |
| Published-skill produce is one checklist; other pins and PR landing are later optional steps; `release/v*` accepts the partial produce | One process; deterministic; earliest controllable; in-repo (Skill type / ADR 0010 bind + host ruleset as the landing half of the same produce contract) | **Survives** |

---

## 8. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** Published-skill produce must be default-closed on every pin that names those bytes, and that produce must not be able to update `origin/release/v*` until those pins are consistent. A skill edit is incomplete unless the identity registry (when the path is registered), the install-hash list (derived), and gate-set ratification (when the path is a member) are updated or the change is refused in the same produce — and the host refuses a direct push of a partial produce onto the release line.

That is the process that produced an unregistered Planit skill, nine stale install fingerprints, an unsigned gate-set, and a no-PR release-line land as one class.

---

## 9. Prevention test

> If **Skill produce had refused MET unless every hash pin that names the edited `SKILL.md` bytes was updated in the same change, and `release/v*` had refused non-PR pushes unless fitness (already including `planit-skill-identity`) was green,** had been in place **before** walkthrough step 5, **`d4b4648` updating `origin/release/v0.4.0` with Planit bytes `0e0493b4…` while the registry still said `85a11ef6…`** could not have occurred because **the Skill-type gate would refuse the produce without the pin updates, and GitHub would refuse the ref update without a PR whose required fitness job already fails `PLANIT_IDENTITY`.**

**Completed:** yes (mechanism: produce-time pin coupling + host landing refuse; the owner hook is how the same identity command is seen locally after the land).

---

## 10. Contributing factors (optional)

- Walkthrough step 5 mentioned “Refresh Planit identity” as prose; ADR 0054 / Skill recipe do not bind that sentence, so `SKILL_AUTHOR:MET` closed the step.
- Walkthrough step 8 **intends** an unsigned gate-set until the owner signs last — so `da90b90` is consistent with that split, and is part of the same class (partial produce on the release line).
- ADR 0046 hook is `beforeSubmitPrompt`, not `pre-commit` / `pre-push`.
- Cloud “open a PR” briefing conflicts with ADR 0044 / `/release` “commit on `release/v*`”; the session resolved toward the hub brief.
- Fitness on `release/v0.4.0` was already red, so a new red identity fail was not a novel stop signal.
- `.nlc/planit-change-evidence.json` still records `85a11ef6…` (stale evidence; not the registry).

---

## 11. Preventive action (not done in this record)

RCA only. No remediation commit.

| Field | Value |
| ----- | ----- |
| Action | Track one produce-contract change: Skill type + handoff refuse unless all pins that name the edited skill bytes are updated in the same change; add a GitHub ruleset that forbids direct pushes to `release/*` and requires the fitness job |
| Owner | hub (human manager) |
| Path / artifact | `content-types/HOW-TO-ADD.md` Skill gate table; `integrity/skill-author-checklist.json` (or a bound identity/install-hash check id); GitHub ruleset on `release/v*`; ADR 0010 / 0046 / 0054 binders |
| Verification | A landmine that edits `.agents/skills/planit/SKILL.md` without touching `planit-skill-registry.json` is `PLANIT_IDENTITY:NOT_MET` **and** Contribution Gate refuse; `git push` to `release/v*` without a PR is rejected by GitHub |
| Belief / gate touch (ADR 0025) | Unsuitable process: generate-then-one-checklist. Touches ADR 0010 (gate after every generate), ADR 0046 (identity pin), ADR 0054 (Skill author contract), Skill type recipe, `planit-skill-identity` / install-verify / gate-set-manifest, and the `release/v*` landing rule in `RELEASE.md` |

---

## 12. Follow-up (candidates only — do not implement here)

**Class this root covers:** any produce that mutates a pinned published artifact (skill, install fingerprint, gate-set member) can satisfy one named gate, skip the other pins, and update `origin/release/v*` without a PR.

| # | Candidate | Prevents | Does not prevent |
| - | --------- | -------- | ---------------- |
| 1 | Bind Skill produce: refuse MET unless every pin that names those `SKILL.md` bytes is updated in the same change (identity registry when registered; run `nlc-install-hash-update.py` for published skills; do not land an unsigned gate-set regenerate as “done”) | Unregistered skill edits; stale install fingerprints; treating `SKILL_AUTHOR` as a complete produce | A determined direct push of a *complete* pin update onto `release/v*` with no PR |
| 2 | GitHub ruleset: no direct push to `release/*`; required check = `fitness` (already fails `planit-skill-identity`) | Unreviewed landing; this exact no-PR push | Local unregistered edits until someone opens a PR; walkthroughs that still split pins across commits |
| 3 | Repo `pre-push` running identity + install-verify + gate-set-manifest | A hook-respecting push of mismatched pins | Cloud/agent-hooks that are not this script; hook bypass; host still accepts the ref if hooks are absent |

**Recommend (1), with (2) as the landing half of the same produce contract.** (1) is the earliest controllable refuse (ADR 0010 / Skill type). (2) is what makes the already-failing CI job actually stop `origin/release/v*` from moving. (3) is detection-only and is how the owner hook already behaves — after the land.

---

## 13. The root (one sentence) — Climb 1 (superseded)

Published-skill produce is allowed to treat a single author checklist as the finish line and land those bytes on an unprotected release line, while identity pins, install fingerprints, and owner-signed gate-set remain optional later steps.

Climb 1 names the **condition**. Climb 2 asks what **created** that condition (owner, 2026-10-25): “How could this condition be created where we made a mandate for a signature and still allowed the skill edits to treat it as optional? What created that condition?”

---

## 14. Climb 2 — what created “pins are optional later steps”

**Scope (user words):** “RCA ONLY, no remediation changes.” “Climb one level above the current root: find what CREATED the condition that signature/identity pins are optional later steps for skill produce.” Four evidence questions as numbered in the request.

**Climb 1 root (too low):** the Skill produce finish line is one author checklist; identity, install fingerprints, and owner-signed gate-set are later optional steps; `release/v*` accepts the partial produce.

**This climb’s error condition:** a signature/identity **mandate** exists, and Skill produce is still allowed to treat that mandate as optional.

---

### Q1. How were the owner-signature mandates expressed?

**After-the-fact checks that report red on the result tree.** Policy text sometimes says “before merge” / “handoff REFUSE,” but the compiled form is a fitness/verify detector. None of these mandates is a precondition on Skill produce or on landing to `release/v*`.

| Mandate | Date / SHA | What the text says | What was wired |
| ------- | ---------- | ------------------ | -------------- |
| **ADR 0051** SG2 (hub-own produce — gate-set bytes need owner receipt) | 2026-10-11 `f0a0216` | **P-GATE-SET-RATIFY:** “content hash change requires human manager receipt **before merge**.” **R-GATE-SET-NO-SILENT-WEAKEN:** a produce package that changes member bytes without a receipt is “incomplete (**handoff REFUSE**).” Same row’s **codified constraint** is already a detector: “(to implement) `fitness-gate-change-receipt` … **NOT_MET** when diff touches gate-set paths.” **Decision 5:** “Implementation of codified constraints is follow-on work; this Proposed record **does not wire CI**.” | Follow-on wiring `d79e03b` (2026-10-13) + **ADR 0053** (text retrofit, Proposed 2026-10-13): in-force check is `fitness-gate-set-manifest` on the tree. **ADR 0053** item 2: the receipt filename is stale; SSOT is `integrity/gate-set-baseline.manifest.sha256` plus its OpenPGP sidecar |
| **ADR 0052** (owner OpenPGP ratification — amends 0051) | 2026-10-11 `cd384ea` (signed `#15`) | Context: “Agents commit pasted armor **unchanged**; they **never create ratification**.” Decision 4: “**Stamp / fitness (completion confirmation only)** … Unsigned, wrong key, hash mismatch, tampered manifest, or **pending** → **NOT_MET**. **No tool may write a ratified entry.**” Consequences: “Until step 2 lands, **no CI check enforces this**; the PM holds the merge.” | Same wiring: `fitness-adr-owner-sidecar` (C6) and `fitness-gate-set-manifest`. C6 in `.nlc/produce-package.json` at `d79e03b` is already **`exit_status`: `REFUSE`**, and `ssot_exit_status` is “owner ratification of legacy ADR sidecars and the **unsigned** gate-set manifest is **outstanding**.” Produce is allowed to finish with signing unfinished |
| **Gate-set sidecar** | Generator `1bce2eb` (2026-10-12) | `tools/generate-gate-set-baseline-manifest.py` header: “Regenerate … from gate-set paths **(no ratification)**.” | A legal produce step writes an unsigned member list. The sidecar check then paints the tree red. Regenerating unsigned is a named ship step (`1ee783d` 2026-10-21 “Regenerate **unsigned** gate-set manifest…”) |
| **ADR 0046** Planit identity registry | 2026-10-08; still **Proposed** / “Pending a redraft” (`9e3e442` 2026-10-13) | Decision 3: “**Intake fails** when the loaded path or the loaded bytes do not match the registry.” Decision 5: Cursor `beforeSubmitPrompt` hook; other harnesses run `fitness-planit-identity.py --skill-only`. | `integrity/adr-gates.json` binder **0046** → `tools/fitness-planit-identity.py`. `integrity/releasable-gates.json` puts `planit-skill-identity` on the **verify** profile (runs after the tree exists). Not a produce-time refuse on `SKILL.md` writes |

**Quoted design of “red, not refuse produce”:**

- **ADR 0051** Decision 5 (line 105): “this Proposed record does not wire CI.”
- **ADR 0052** Decision 4 (line 50): “Stamp / fitness (completion confirmation only).”
- **ADR 0052** line 40: “Until step 2 lands, no CI check enforces this.”
- Hub produce package (`d79e03b`, unchanged at this tip): C6 **REFUSE** + “unsigned gate-set manifest is outstanding.”
- C8 (`tools/nouns/fitness_no_tool_writes_ratification/fitness_no_tool_writes_ratification.py` line 1): “no tracked tool writes `*.approval.asc`.” A producer **cannot** complete the signature.

Published `SKILL.md` files **are** gate-set members today (`integrity/gate-set-baseline.manifest.sha256` lines 11–20 include `.agents/skills/planit/SKILL.md` and the other published skills). **ADR 0053** item 1: membership is **derived** by `derive_gate_set_paths` from CI workflow seeds — not a hand-kept Skill-type list. So the signature mandate covers skill bytes as members, but only through the same after-the-fact manifest+sidecar detector. `d4b4648` already rewrote the **unsigned** manifest in the skill-repair commit; `da90b90` did it again. That is the mandate’s designed produce path, not a miss.

---

### Q2. Were the Skill recipe, the skill-author checklist, and `/release` derived from those mandates?

**Authored separately.** No import, no derived list, no reference to **ADR 0051**, **ADR 0052**, the gate-set sidecar, or the Planit identity registry. Each produce recipe must restate those mandates by hand — and none of them did.

| Produce surface | When / SHA | What it binds | Mentions 0051 / 0052 / 0046 / sidecar / identity registry? |
| --------------- | ---------- | ------------- | ---------------------------------------------------------- |
| `integrity/skill-author-checklist.json` | 2026-10-21 `11a904c` | `frontmatter-yaml`, `in-skill-links` only. Commit body: “Same checklist SSOT (**frontmatter YAML plus in-skill links**).” | No |
| **ADR 0054** (published-skill author contract) | 2026-10-24 `bcb2f95`; Accepted `15c9bb0` | “**Checks now (discovered problems):** `frontmatter-yaml` … `in-skill-links`.” Context: “This record does **not** add Skill as a content type. … This record does **not** repair current hub skills.” Rejected: adding Skill as a type; repairing live skills | No. Rationale is **RCA 2026-10-20** (YAML `name:` / dead install links), not hub-own produce or identity |
| Skill type recipe (`content-types/HOW-TO-ADD.md`) | 2026-10-25 `4f3caf2` “Add Skill as a content type **pointed at the author checklist**” | Gate table = that checklist. Steps 1–6 end at `nlc-skill-author-check.py` + Contribution Gate CG-R2/CG-R3 | No. `git grep` of `approval.asc`, `sidecar`, `0052`, `gate-set` in `HOW-TO-ADD.md` is empty. The **ADR** type recipe (same file, lines 69–78) also has no sidecar row |
| `fitness-skill-content-type.py` | same `4f3caf2` | Module docstring: “recipe gate is the published-skill author checklist.” The binder **requires** the recipe to name `nlc-skill-author-check.py` and `skill-author-checklist.json` | Locks the separate checklist. Does not require identity or signing |
| `/release` skill | last material identity work `605cd17` (2026-10-10, **ADR 0050**) before the 0051/0052 wave; later edits are current-ship prose and the `d4b4648` YAML repair | Closeout = `ci_fitness.py` CI:MET, FINDINGS tree hash, inference record. Ship prove is a later phase | `git grep` of `0051`, `0052`, `0046`, `planit-skill-registry`, `gate-set-baseline`, `approval.asc` in `.agents/skills/release/SKILL.md` is empty |

**Contrast — what *is* derived from 0051/0052:** `integrity/adr-0051-0052-rules.json` must equal `tools/derive-adr-0051-0052-rules.py`; `integrity/adr-gates.json` maps those ADRs to **fitness** tools. That derivation feeds **detectors**, not type recipes.

**ADR 0010** (2026-09-16, gate immediately after every generate) says skills “inherit this rule.” Inheritance here means “run **that artifact’s** gate.” The Skill artifact’s gate was later defined as the two-item author checklist. **PLANIT-ORCHESTRATION** X6 is “gates of ADRs **bound to this action**” (per-action), not “gates of every mandate that names a touched path.” **GATE-STD** is “every touched path has a default-closed gate or N/A” — and the Skill path’s named gate is `SKILL_AUTHOR`.

The 0.4.0 TODO repair row restates the split in operator words: “Repair current published skills so … is `SKILL_AUTHOR:MET` (**plain `name:` + in-skill links only**).”

---

### Q3. Is this a general pattern? Other mandated artifacts with the same gap

**Yes.** Mandates are compiled as detection gates on results (`integrity/releasable-gates.json`, `ci_fitness`, `adr-gates.json`). There is **no** mechanism that makes every producer that touches a mandated artifact inherit the mandate. Contribution Gate **CG-R2** only refuses a skipped **type-recipe** step. If the recipe never imported the mandate, CG-R2 cannot fire.

| Mandated artifact | Mandate | Detector (reports red) | Produce recipe that touches it | Inherits the mandate? |
| ----------------- | ------- | ---------------------- | ------------------------------ | --------------------- |
| Published `SKILL.md` (also a **derived** gate-set member) | 0051/0052 sidecar + 0046 identity (Planit) + install fingerprints | `fitness-gate-set-manifest`; `planit-skill-identity`; `nlc-install-verify` | Skill type + author checklist + `/release` | **No** (this incident) |
| Accepted ADR files | 0052 C6 sidecar | `fitness-adr-owner-sidecar` | ADR type recipe (`HOW-TO-ADD.md` lines 69–78): sequence, slug, required fields, index, cross-links | **No** sidecar / Content-SHA256 step |
| Gate-set members generally (`tools/fitness-*.py`, `tools/assert-*.py`, `integrity/releasable-gates.json`, …) | 0051 SG2 / 0052 manifest+sidecar | `fitness-gate-set-manifest` | No “fitness-tool” type recipe. Generator header: **no ratification** | **No** — unsigned regenerate is the produce step |
| `integrity/planit-skill-registry.json` | 0046 path + `content_sha256` | `fitness-planit-identity` (intake + verify) | None. Hand-kept; last content change `5bd6113` | **No** generator, no Skill-type step |
| `integrity/nlc-install-hashes.json` | Piped-install fingerprint list | `nlc-install-verify` | Updater `nlc-install-hash-update.py` exists; no type recipe requires it | **No** |
| `FINDINGS.md` `last_pass_tree_hash` / `integrity/hub-content-tree-hash.txt` | **ADR 0050** (evidence is content, not history) | `fitness-findings-last-pass-fresh` (`hub-content-tree-fresh` on verify) | `/release` Step 1A names it as **ship closeout**, not as an inherited produce gate | **No** for Skill/ADR/tool produce |
| `integrity/nlc-version.json` + `integrity/hub-release-record.json` | **ADR 0045** ship identity | release tag/state gates | `/release` / `./release` later | **No** for ordinary produce |
| `integrity/full-nlc-audit-inference-record.json` | `/release` inference pin | audit freshness | `/release` Step 1A.5 only | **No** |
| `integrity/owner-keys/` + `TRUSTED_FINGERPRINTS` | 0052 pinned key / C9 retired denylist | `fitness-owner-key-trust`, `fitness-retired-key-denylist` | No key-rotation type recipe | **No** |
| `integrity/known-bad-cases.json` | 0051 known-bad SSOT (C5) | `fitness-known-bad-ssot` | No | **No** |
| `.nlc/planit-change-evidence.json` | 0046 decision 6 (tree hash with identity) | hub compile when wired | No Skill-type step | **No** (Climb 1 already recorded it stale at `85a11ef6…`) |

Same class: a mandate lives in a fitness binder; the producer of the named bytes has a different local finish line.

---

### Q4. Why that design was chosen

Signing was framed as a **final human step**, and mandates as **detectors on results**, on purpose.

1. **RCA 4** (2026-10-11, record kept outside this repository; cited on **ADR 0051** line 9): agents weakened checks, broadened exemptions, or rewrote approval receipts to obtain CI green. **ADR 0051** rejected “CI green as terminal finish line” and forbade producer hand-update of receipts. The chosen compile was **property-leaf fitness** (C1–C11), not a produce-recipe import.

2. **RCA 5** (2026-10-11, outside this repository; cited on **ADR 0052** line 13): “hash-only registries let producers rewrite stamps without the owner's act.” The two-actor principle (human manager ratifies, agents produce) was compiled as: **only** the owner’s clearsigned statement counts; **agents never create ratification**.

3. **C8** (`d79e03b` 2026-10-13) makes that compile a hard gate: no tracked tool may write `*.approval.asc`. Combined with a generator whose job is “no ratification,” the **only legal produce path** is: mutate member bytes → write an **unsigned** manifest → leave the sidecar stale → fitness **NOT_MET** → owner signs later. Completing the mandate inside Skill produce is **forbidden**, not omitted.

4. **Human-judgment split** (`docs/nlc/HUMAN-JUDGMENT-GATES.md` lines 18–23): “**ADR / rule adoption** — Human sets ADR Accepted; agent does not ratify.” Same file: ship is after verify, human signed.

5. **Production-trunk + sidecar-last as the ship playbook.** **ADR 0044** puts unreleased work on `release/v*`. TODO and release notes encode unsigned-then-sign as two commits:
   - `TODO` lines 644, 654 (done) and **668** (still open on the 0.3.3/0.4.0 line): “Owner clearsign of the unsigned gate-set manifest (**sidecar last**; no verify-deep after sidecar).”
   - `docs/adoption/RELEASE-v0.3.1.md` lines 22–23: “Refresh the content digest and **unsigned** gate-set manifest (`0a9bb47`)” then “Add the owner-signed gate-set manifest sidecar (`0f7d896`).”
   - `docs/adoption/RELEASE-v0.3.2.md` lines 20–22: same split (`9de2d26` unsigned, `89fb12b` sidecar).
   - Walkthrough step 8 (Climb 1): owner sidecar last. The incident session followed that playbook.

6. **Skill contract scoped to the YAML RCA only.** **RCA 2026-10-20** + **ADR 0054** were a later, separate produce (2026-10-21…25). They bound the two discovered load problems. They did not import 0051/0052/0046. **ADR 0046** was left Proposed / pending redraft, so identity stayed an intake/verify detector.

**What this created:** a mandate that is real (CI goes red; owner hook denies Planit) and a Skill produce that is also real (`SKILL_AUTHOR:MET`) because the mandate was never a precondition on that produce. Optional later signing is not a walkthrough accident. It is the 0051/0052/C8 compile.

---

### Climb 2 — the one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this condition from arising**?

**Answer:** Owner-signature and identity mandates must be compiled as **inherited produce preconditions** on every producer that touches a named artifact — a derived mandate list the type recipe / produce skill **imports**, not a result-tree detector plus an owner-last sign step that each recipe must restate by hand.

If that had been in force before the Skill checklist and the 0.4.0 walkthrough, `SKILL_AUTHOR:MET` could not have been a complete Skill produce while Planit identity, install fingerprints, and the gate-set sidecar stayed later. C8 can still forbid tools from writing armor; the refuse is “this produce is incomplete,” not “regenerate unsigned and continue.”

**Prevention test:** If **every producer that touches a path named by a mandate had imported that mandate as a produce-time refuse (derived list, not hand restatement), and an unsigned mutation of a signed pin had been handoff incomplete rather than a later sign step,** had been in place **before** walkthrough step 5, **`d4b4648` / `da90b90` treating `SKILL_AUTHOR:MET` as done while the registry still said `85a11ef6…` and the sidecar still named `8ffa1481…`** could not have occurred because **Skill produce would have inherited 0046 / 0051 / 0052 / install-hash and refused MET without those pins, instead of running a separately authored two-item checklist.**

**Completed:** yes (mechanism: mandate → producer inheritance; the unsigned-then-sign playbook is how the current compile made inheritance unnecessary and, under C8, impossible to finish in-agent).

---

### Climb 2 — the root (one sentence)

Mandates for owner signatures and identity pins were compiled as after-the-fact result-tree detectors and an owner-last sign step that produce tools are forbidden to complete, while Skill (and other) produce recipes were authored as separate local checklists with no import of those mandates.

---

### Class this climbed root covers

Any producer that touches a mandated artifact can finish its own recipe while the mandate stays a red CI/verify row or a later human sign — because nothing makes the producer inherit the mandate.

That class includes this unregistered Planit skill, an unsigned gate-set regenerate, a stale install-fingerprint list, an Accepted ADR without a sidecar, a fitness-tool edit that only rewrites the unsigned manifest, and a FINDINGS edit that leaves `last_pass_tree_hash` for `/release` closeout.

---

### Revised remediation candidates (not done in this record)

Climb 1 candidates (bind the Skill checklist to every pin; GitHub ruleset; pre-push script) treat the **condition**. They do not remove the compile that **creates** “optional later.”

| # | Candidate | Prevents | Does not prevent |
| - | --------- | -------- | ---------------- |
| 1 | **Mandate inheritance:** one derived list (paths named by 0051/0052/0046/install-hash/0050/…) that every type recipe and produce skill **imports**. Touching a named path makes those gates produce-time refuse. Contribution Gate CG-R2 fails a recipe that omitted an imported mandate. Do not hand-restate per recipe | This class: Skill/ADR/tool/FINDINGS produce that MET a local list while a mandate on those bytes stays later | A determined host push of a **complete** inherited produce; owner still must sign because C8 forbids tools writing armor |
| 2 | **End unsigned-then-sign as a complete produce:** regenerate-without-sign is handoff incomplete. Keep C8 (no tool writes `.approval.asc`). Change the playbook: do not land, and do not mark the step done, until the owner has signed **or** the mutation is refused. Delete “sidecar last” / “unsigned gate-set” as a success path on `release/v*` | The designed split that made `da90b90` and v0.3.1/v0.3.2 notes look correct | A Skill recipe that still does not import identity/install-hash if inheritance (1) is skipped |
| 3 | Climb 1 landing half (GitHub ruleset: no direct push to `release/*`; required fitness) | Unreviewed red land of a partial produce | The next produce session that still treats `SKILL_AUTHOR` as done locally |

**Recommend (1) as the climbed one thing**, with (2) as the same compile (precondition, not detector-plus-later-sign). (3) remains the host backstop from Climb 1.

RCA only. No remediation commit.
