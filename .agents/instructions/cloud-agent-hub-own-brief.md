# Cloud agent brief — hub material produce (ADR 0051)

Use this template when a cloud agent brief scopes **hub material** work on this repository (stabilization, integrity surfaces, gate-set edits, or codified constraints under [ADR 0051](../../adrs/0051-hub-own-produce-principles.md)).

## Required brief content

1. **Property leaf goals (SG1):** List each finish-line *property* as an opaque leaf id plus plain-language statement. Terminal success must **not** name only CI MET, fitness green, or GitHub Actions success (`R-HUB-EXIT`).
2. **Forbid weaken (R-HUB-BRIEF-FORBID-WEAKEN):** The brief must explicitly forbid weakening a check, broadening exemptions, or rewriting approval or gate-change receipts to obtain MET.
3. **Gate-set edits (SG2):** Any change under the ADR 0051 gate-set table requires an updated `integrity/gate-change-receipts.json` entry via **`python3 tools/seed-gate-change-receipts.py`** only after human manager ratification — produce roles do not hand-edit receipt hashes.
4. **Role separation (SG3):** If the same package touches both gate-set members and graded subject paths (see `integrity/hub-gate-diff-profile.json`), `producer_role` and `adversarial_auditor_role` must differ and the package must include an `adversarial_reviewer_receipt`.

## Produce package

Hub material PRs must set `"hub_material": true` on `.nlc/produce-package.json`, declare `hub_goal_tree` with `property_leaf_goals` (each with `leaf_id`, `statement`, `exit_status`, and evidence path), and list `changed_paths` for the diff scope.

## Rule against regress

Codified constraints grade work or work products only. Do not add checks that judge another check’s logic. Known-bad Candidates for each constraint are verified directly (no wrapper gate over those fixtures).
