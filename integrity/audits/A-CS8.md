# Audit A-CS8: Task/board SSOT exit evidence checklist item

## Checklist item

**CS8.** Task/board SSOT exit evidence present in produce package (`ssot_leaf_ids` + `ssot_exit_status`); missing evidence refused (P-020).

## Audit criteria

**Met** iff:

1. The produce package directory declares SSOT exit evidence (in ADVERSARIAL.md or dedicated SSOT evidence file).
2. `ssot_leaf_ids` present with ≥1 opaque leaf id.
3. `ssot_exit_status` present with non-empty status value.
4. Leaf ids are non-empty opaque strings (shape may be UUID; product API validation is out of BBA scope).

**Not met** otherwise; enumerate missing/empty fields.

## Evidence

- `reviews/pr-*/ADVERSARIAL.md` — `ssot_leaf_ids` / `ssot_exit_status`
- Or `reviews/pr-*/SSOT-EXIT.md` — dedicated evidence file (optional)

## Related

- S8, CS7, P-020 — ADR 0005
