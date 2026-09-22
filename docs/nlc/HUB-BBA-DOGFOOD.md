# Hub BBA dogfood (X4)

Hub *process* is NLC. Hub *emit* — when this repo writes a compiled-system tree — is BBA.

This note is the v1 binder. It does not rewrite hub interiors.

## Emit paths in this repo

| Path | Must emit |
|------|-----------|
| `tools/nlc-init.py` | adopter tree with `goals/`, `nouns/` or documented equivalent |
| `tools/nlc_rule_emit.py` | rule instances, not ad-hoc labels |
| goal scaffold / delta-regen | goal files that call verbs; never write noun fields |

## Not this pass

Rewriting `tools/*.py` interiors into noun/verb/goal packages. Tracked as X4 remaining on [`FINDINGS.md`](../../FINDINGS.md).
