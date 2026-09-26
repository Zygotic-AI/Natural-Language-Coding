# RCA: Trunk normalize reused local v0.2.0 tag while remote shipped commit differed

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — zero-parameter `./release` from impure `main`  
**Status:** corrected — local and origin `v0.2.0` are the same annotated tag (`d853c4af` tag object, commit `023bad1`). Comparing `ls-remote` tag-object id to `tag^{commit}` was a false divergence. Shipped-baseline resolution must use the peeled commit (`refs/tags/v0.2.0^{}`).

---

## 1. Error condition

**Evidence (observed):**

- Command: `./release` on **`main`** with large dirty tree (`main(+425/-195)`).
- Infer: **`target=0.3.0`**, action **`normalize_main_trunk`**, tag baseline **`v0.2.0`** (already shipped).
- Trunk step output:

  ```text
  main now at v0.2.0 (local only; no push).
  HEAD is now at 023bad1 Remediate release PR CI: binder, RCA, shared shipped baseline.
  ```

- Step 0b: **`RELEASE_SHIPPED_TAG:MET tag=v0.2.0 commit=023bad16c1ff`** (same as **`origin/main`**).
- Workspace repro (post-incident):

  ```bash
  git rev-parse v0.2.0^{commit}
  # 023bad16c1ff969d5c3b760fcaa131bf2828fa3c
  git ls-remote origin refs/tags/v0.2.0
  # d853c4af277b95305a2f829a20cbae3d7e7c548e
  ```

- Step 3 verify-deep detached at **`v0.2.0^{commit}`** with **dirty working tree** on **`release/v0.3.0`** → **`CI:FAIL release signed`**; second **`./release`** → **`Resume: release/v0.3.0 pushed; waiting for merge`** (in-flight line, not a re-ship of v0.2.0).

**Inferred:**

- Operator experience: tooling **reused the already-released v0.2.0 label** for trunk reset and shipped-baseline verify while **`main` never moved to the canonical remote shipped commit**.

**Mechanism confirmed on reproduction:** yes — local peeled **`v0.2.0^{commit}`** ≠ **`origin` refs/tags/v0.2.0**; orchestrator **`git reset --hard v0.2.0^{commit}`** left **`main`** at impure **`023bad1`**.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Trunk normalize + verify-deep | Reset/detach using **local** tag peel → **023bad1** |
| 3 | `scripts/nlc-release.sh` | **`${shipped_tag}^{commit}`** for reset and verify-deep |
| 2 | `nlc_release_shipped_tag_audit.py` | Audited **local** `tag^{commit}`; **MET** despite remote divergence |
| 1 | `release_main_purity` | Compared **`main`** to **remote** tag commit (correct) but normalize did not use that commit |

**Furthest controllable upstream point:** **`release_tags` shipped-baseline SSOT** — one resolver for reset, verify-deep, and shipped-tag audit.

---

## 3. Impact / scope

- ADR 0044 “production trunk normalize” **no-op** relative to true shipped artifact when local tag is wrong.
- Misleading **`RELEASE_SHIPPED_TAG:MET`** while local tag diverges from **`origin`**.
- Wasted **`release/v0.3.0`** prepare/resume cycle; verify-deep at wrong baseline with dirty tree.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-25 | `./release` infer **0.3.0**, trunk normalize, **`release/v0.3.0`** created |
| 26-09-25 | Preflight/shipped audit **MET** at **023bad1**; verify-deep **NOT_MET** |
| 26-09-25 | Second **`./release`** → resume **`await_merge`** for **v0.3.0** |
| 26-09-25 | RCA + **`canonical_tag_commit`** + divergence gate in shipped audit |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** **Hub release must resolve the shipped baseline commit from `origin` refs/tags (via `canonical_tag_commit`) for trunk normalize and verify-deep, and refuse `RELEASE_SHIPPED_TAG:MET` when local `tag^{commit}` differs from that remote commit.**

---

## 6. Prevention test

> If **`canonical_tag_commit` + local/remote divergence NOT_MET in shipped-tag audit** had been in place before the failure, **trunk normalize leaving `main` at 023bad1 while `origin` v0.2.0 is d853c4af** could not have occurred because **reset/verify would target d853c4af and step 0b would block until local tags match remote**.

**Completed:** yes — `python3 tools/nlc_release_shipped_tag_audit.py --check` exits **1** with divergence message on this workspace.

---

## 7. Contributing factors (optional)

- **`release/v0.2.0`** still listed in **`RELEASE_CONTEXT`** candidates (now annotated **shipped — closed**).
- Resume **`await_merge`** for **`release/v0.3.0`** after failed prepare is correct resume semantics, not re-shipping v0.2.0.
- Dirty tree on **`release/v0.3.0`** during detached verify-deep (separate hardening: commit/stash policy on release line before baseline verify).

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | SSOT **`canonical_tag_commit`** in **`release_tags`**; wire infer **`INFER_SHIPPED_COMMIT`**, orchestrator reset/verify-deep, shipped-tag divergence gate |
| Owner | TBD (hub maintainers) |
| Path / artifact | `tools/nouns/release_tags/release_tags.py`, `scripts/nlc-release.sh`, `tools/nlc_release_shipped_tag_audit.py`, `tools/nouns/release_infer/release_infer.py` |
| Verification | `python3 tools/nlc_release_shipped_tag_audit.py --check` (expect NOT_MET until `git fetch origin --tags && git tag -f v0.2.0 $(git ls-remote origin refs/tags/v0.2.0 \| awk '{print $1}')`); dry-run trunk normalize shows reset to **d853c4af** |
| Human acceptance | `pending` |
| Implementation route | **`/planit`** after acceptance — cite this RCA path in the plan |

---

## 9. Follow-up (detection only if prevention insufficient)

- Operator: align local **`v0.2.0`** with **`origin`** before next ship (see shipped audit fix line).
- Optional: fail verify-deep when release-line working tree is dirty before detach.
