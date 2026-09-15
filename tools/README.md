# Tools

Enforcement and scaffolding that make the charter real.

## Commands

```bash
python3 tools/assert-invoice-violation-fails.py
python3 tools/assert-verb-path-violation-fails.py
python3 tools/assert-adjective-locality-violation-fails.py
```

| Tool | Proves | Does not prove |
|------|--------|----------------|
| [`fitness-no-noun-field-writes.py`](fitness-no-noun-field-writes.py) | R5 / C4 field assignment | Verb path, copied adjectives |
| [`fitness-verb-path.py`](fitness-verb-path.py) | R6/C5 v1 persistence escapes | Full "every mutation is a verb" |
| [`fitness-adjective-locality.py`](fitness-adjective-locality.py) | R24 v1: named tokens + field math outside the noun | Duplicated predicates with different spelling (C19) |

R6/C5 stay unbound. R24 should be rebound to `fitness-adjective-locality.py` (matrix field still stale).

## Adjective locality v1

Tokens: `domain/<noun>/adjectives.txt`. Field math: operators on names in `fields.txt` outside the noun.

```bash
python3 tools/fitness-adjective-locality.py examples/invoice-locality-violation  # NOT_MET
python3 tools/fitness-no-noun-field-writes.py examples/invoice-locality-violation  # MET
python3 tools/fitness-verb-path.py examples/invoice-locality-violation              # MET
```

## Agent nouns

`AGENT.md` heading is `## Adjectives`. Legacy `## Invariants` still passes.

## Still planned

A5 taint / one-boundary. A7 broader escapes. Contract presence. Generated graphs.
