# TODO product UC completion (SSOT with USE-CASES)

When marking a row **done** under **`TODO` → “Build a compiled system — use-case dependencies”**:

1. Read [`integrity/uc-product-status.json`](../../integrity/uc-product-status.json) — set `product: "closed"` only when the USE-CASES spine story is honestly in force (v1 or full).
2. Read [`docs/USE-CASES.md`](../../docs/USE-CASES.md) spine + **Needed (expansion)** — `EXPANSION-ONLY` rows are not blockers for product `@done`.
3. If product is not closed in JSON, you may only mark **v1 binder** work done:
   - The `✔` line must include **`v1 binder`**, **`partial`**, or **`stub`** in the same line.
   - Leave a sibling **`☐` product** row, or update `uc-product-status.json` + USE-CASES in the same change.
4. Do **not** mark a UC `@done` because `tools/fitness-*-binder.py` is MET alone.
5. Before claiming “complete,” run:
   - `python3 tools/fitness-todo-use-cases-ssot.py`
   - `python3 tools/fitness-jobs-todo-sync.py`
   - Planit-style audit in the **same turn** when closing product rows.

Enforced in CI: [`tools/fitness-todo-use-cases-ssot.py`](../../tools/fitness-todo-use-cases-ssot.py), [`tools/fitness-jobs-todo-sync.py`](../../tools/fitness-jobs-todo-sync.py).
