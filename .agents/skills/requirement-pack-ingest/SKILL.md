---
name: requirement-pack-ingest
description: Ingest external policy markdown into candidate ADRs/rules for human ratification (requirement packs v0.2). Use before pack export.
disable-model-invocation: true
---

# Requirement pack ingest (v0.2)

Human ratifies every row. The compiler does not adopt policy from chat memory.

## Gate (default-closed)

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| Source file | yes | Repo-relative markdown path exists |
| Ratify forbidden | yes | No direct edits to `rules/adopted.json` or Accepted ADRs without `/interview` |
| Output | yes | `.nlc/pack-ingest-candidates.json` written |

## Procedure

1. Confirm outcome: import external requirements into this repo’s ADR/rule SSOT.
2. Run `./nlc maintainer pack-ingest <source.md>` (or `python3 tools/nlc-pack-ingest.py`).
3. Review `.nlc/pack-ingest-candidates.json` with the human.
4. Route to **`/interview`** → ratify Proposed ADRs → `./nlc maintainer rule-runner --materialize`.
5. Export when green: `./nlc pack export` (see Hub v0.2 packs docs).

## Done signals

- `PACK_INGEST:MET` on stdout
- Human has a numbered ratification list from candidates file
- No Accepted ADR cites ingest output without review
