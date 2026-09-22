# [Audit](../../docs/TERMS.md#audit) A-CS8: Task/board [SSOT exit evidence](../../docs/TERMS.md#ssot-exit-evidence) checklist item

## Checklist item

**CS8.** Task/board [SSOT exit evidence](../../docs/TERMS.md#ssot-exit-evidence) present in [produce package](../../docs/TERMS.md#produce-package) (`ssot_leaf_ids` + `ssot_exit_status`); missing evidence refused (P-020).

## [Audit](../../docs/TERMS.md#audit) criteria

**[Met](../../docs/TERMS.md#met)** iff:

1. The [produce package](../../docs/TERMS.md#produce-package) directory declares [SSOT exit evidence](../../docs/TERMS.md#ssot-exit-evidence) (in ADVERSARIAL.md or dedicated SSOT evidence file).
2. `ssot_leaf_ids` present with ≥1 opaque leaf id.
3. `ssot_exit_status` present with non-empty status value.
4. Leaf ids are non-empty opaque strings (shape may be UUID; product API validation is out of BBA scope).

**Not [met](../../docs/TERMS.md#met)** otherwise; enumerate missing/empty fields.

## Evidence

- `reviews/pr-*/ADVERSARIAL.md` — `ssot_leaf_ids` / `ssot_exit_status`
- Or `reviews/pr-*/SSOT-EXIT.md` — dedicated evidence file (optional)

## Related

- S8, CS7, [P-020](../../docs/TERMS.md#ssot-exit-evidence) — [ADR](../../docs/TERMS.md#adr) 0005
