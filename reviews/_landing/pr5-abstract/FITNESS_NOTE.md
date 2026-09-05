# Fitness note — P-020 abstract delta (Reed / Quality Architect)

## One-page status

| Item | Status |
|------|--------|
| Prior PR #5 fitness on Notion-named surface | **Superseded** |
| Architecture-scope verdict on Notion-coupled P-020 | **FAIL** |
| Abstract package (this kit) | **Ready for land** (pending Koan apply + adversarial) |

## Why prior MET is superseded

Reed previously scored PR #5 **MET** on the Notion-named produce-package surface (page ids / exit status / `NOTION_*` tokens). That MET assessed package completeness and refuse-pattern wiring **within the product-coupled vocabulary**.

Architecture principle lock for BBA:

- BBA = architecture definition; **tool-agnostic**
- No product brand, MCP, or IDE/agent-product bindings as required vocabulary in charter / AGENTS.md / agent verb field names

Under that lock, Notion-named fields in BBA charter and agent contracts are an **architecture-scope FAIL**, regardless of prior MET/PASS on the coupled surface. Prior adversarial PASS on Notion dogfood does not clear the architecture defect.

## What this kit supplies

Complete landable prose for a delta (preferred on PR #5 branch) or superseding PR:

- Charter Step 2 / S8 / CS8 abstract replacements
- ADR 0005 rewritten + renamed to `0005-ssot-exit-evidence.md`
- Find/replace map for steward / QA / auditor / AGENTS.md / A-S8 / A-CS8 / matrix statements
- Produce package that dogfoods `ssot_leaf_ids` / `ssot_exit_status` only
- Verify script expectations for the abstract surface

Refuse pattern unchanged (same class as S7/P-016). S8/CS8 remain **reference** / **unbound** (P7).

## Dogfood leaf (opaque)

```yaml
ssot_leaf_ids:
  - "3d29d973-ccd7-8158-a1c2-e8d46be9bbef"
ssot_exit_status: "in progress"
```

Opaque leaf id only — not labeled as a product field. Parked prior leaf must not be dogfooded.

## Next

Koan lands the delta from this kit → fitness re-score on abstract surface → adversarial → ship. Reed does not invent further prose unless adversarial returns blockers.
