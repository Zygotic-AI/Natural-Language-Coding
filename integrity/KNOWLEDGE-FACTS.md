# Knowledge facts (UC18)

Interview and bind steps consult **knowledge domains**. Machine-checkable facts live in repo-root [`knowledge/facts.json`](../knowledge/facts.json), not only ADR prose.

## Fact card

| Field | Required | Meaning |
| ----- | -------- | ------- |
| `id` | yes | Stable id (`KF-…`) |
| `scope` | yes | Noun or topic (e.g. `invoice`, `pii`) |
| `statement` | yes | Confirmed truth in plain language |
| `status` | yes | `proposed` \| `confirmed` \| `superseded` |
| `superseded_by` | when superseded | Id of replacing fact |
| `sources` | no | ADR ids or external refs |

## Gate

```bash
python3 tools/validate-knowledge-facts.py [repo-root]
```

Exit 0 = `FACTS:MET`. Exit 1 = `FACTS:NOT_MET` with defects.

Knowledge steward `load-knowledge-domain` (`tools/load-knowledge-domain.py`) reads confirmed facts for scope. New facts: `propose-fact` → human sets `status: confirmed`.
