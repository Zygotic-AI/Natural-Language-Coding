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

## 13. The root (one sentence)

Published-skill produce is allowed to treat a single author checklist as the finish line and land those bytes on an unprotected release line, while identity pins, install fingerprints, and owner-signed gate-set remain optional later steps.
