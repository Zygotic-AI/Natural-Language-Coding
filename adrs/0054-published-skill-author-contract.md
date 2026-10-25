# ADR 0054 — Published-skill author contract

- Status: Accepted
- Date: 2026-10-24
- Deciders: Human manager
- Class: F (integrity / hub produce)
- Corpus: nlc
- Related: [RCA 2026-10-20](../docs/rca/2026-10-20-skill-yaml-terms-link-load-error.md) (skill YAML TERMS-link load error)

## Context

Published skills are installed off this repository. A TERMS-link rewrite treated YAML frontmatter as prose because Skill is not a content type, so `name:` became a glossary link and loaders refused the file. The same publish boundary leaves in-repo `../../../` links pointing nowhere after install.

A growable checklist already exists (`integrity/skill-author-checklist.json`, one CLI `tools/nlc-skill-author-check.py`). Without a dated decision, a use-case, and a presence gate, that checklist looks like helper code and can be deleted or skipped.

This record does **not** add Skill as a content type. That type recipe is a later step. This record does **not** repair current hub skills. Live `SKILL_AUTHOR:NOT_MET` stays until that repair.

## Decision

1. **One list.** The in-force authoring list is `integrity/skill-author-checklist.json`. Add a check by adding an id there, then implementing it in `tools/nouns/skill_author_check/`. Do not create a second checklist.

2. **One command, two moments.** The same CLI runs before release (`release-prep` / `full` audit, `--root .agents/skills`) and after install (`--root` of the copied skills tree). Install may not skip this step behind `NLC_SKIP_VERIFY`.

3. **Checks now (discovered problems):**
   - `frontmatter-yaml` — `SKILL.md` frontmatter parses; `name` is a plain identifier matching the folder.
   - `in-skill-links` — relative markdown links resolve inside the published skills tree.

4. **Use-case.** `goals/hub_skill_author_check/execute.sh` (and `execute.ps1`) wraps that CLI. Hub install invokes this use-case after copying skills. Hub goals stay `execute.sh` / `execute.ps1` only (no `implementation.py`).

5. **Presence.** Fitness refuses MET if hub install no longer invokes `hub_skill_author_check`, or if that use-case no longer invokes `nlc-skill-author-check.py`. Wiping the use-case is a compile fail, not a quiet delete.

6. **Landmine stays red.** `examples/skill-author-check-landmine/` must remain `SKILL_AUTHOR:NOT_MET`. Wiring MET does not require live hub skills MET.

7. **ACTIVE tip.** This record is an ACTIVE tip: the binder applies it. Presence fitness is the compile binder that install still calls the same checklist. Owner ratification is the sidecar beside this file.

## Consequences

- Version class **minor** on the 0.4.0 line (new policy + use-case).
- Owner OpenPGP sidecar sits beside this file (`0054-published-skill-author-contract.md.approval.asc`).
- Current published hub skills remain unloadable until the later repair step. The check stays hard.

## Rejected

- A different post-install list or a second checker.
- Making the install check optional or hiding it behind `NLC_SKIP_VERIFY`.
- Treating linker-skip of published skills as enough (that is a lower cause, not this contract).
- Adding Skill as a content type in this record.
- Repairing live hub skills in this record.
