# No ADR — pull-request offer gate

**Date:** 2026-11-02  
**Change class:** C (orchestration around the existing release prove step). Version class: patch.

No ADR. `tools/pr-offer-gate.py` is the fail-closed offer command from `docs/rca/2026-11-02-pr-offered-before-fitness-success.md`. The body lives in `tools/nouns/pr_offer_gate.py` so the executable-shape check can classify it. The one-level file is a short adapter. The noun path and the adapter are gate-set members, so the manifest hash is regenerated in the same commit. Neither path is a checker-digest member, so the owner signature on `integrity/checker-digest.sha256` stays valid. This does not add a requirement, a verb, or a charter rule. The release skill (`.agents/skills/release/SKILL.md`) is the only offer path, and it calls this command instead of `gh pr create`.

The owner signature on `integrity/checker-digest.sha256` stays valid because this change does not add or edit a checker-digest path.
