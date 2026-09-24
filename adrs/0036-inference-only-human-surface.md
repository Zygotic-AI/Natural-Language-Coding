# ADR 0036 — Inference-only human surface (goal and policy only)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[ADR 0027](0027-emit-from-prose.md) adds a deterministic compiler from constrained prose into pipeline JSON. It does **not** define what humans may contribute on the happy path.

The informal “three things humans focus on” framing in [`docs/nlc/compiler/INTENT-SURFACE.md`](../docs/nlc/compiler/INTENT-SURFACE.md) and [`docs/nlc/compiler/MANIFESTO.md`](../docs/nlc/compiler/MANIFESTO.md) asked humans to hold goals, requirements, and knowledge domains as parallel inputs. That invites humans to author or name derived artifacts (plans, ADR ids, rule ids, anchors, manifests, tags) when the compiler cannot infer them — a process defect, not a human limitation ([ADR 0025](0025-belief-no-blame-climb.md)).

## Decision

On the happy path a human contributes **exactly two** things:

| Human contributes | Compiler infers |
| --- | --- |
| **Goal** — outcome in natural language | Plans, actions, ADR bindings, reverse audit, emit, gates, tests, tags, noun/verb structure |
| **Policy** — constraints, standards, “must / must not” | Requirements, ADRs, rules, and knowledge-domain facts **derived from policy** |

No other human **authorship** is permitted. Ratification, release, and certified [RCA](../docs/TERMS.md#rca) remain human **judgment** over derived artifacts (C24), not authorship of them.

If the compiler cannot derive a binding, it **refuses and reports the gap** — it does not ask the human to supply plans, ADR ids, rule ids, thought anchors, manifests, or tags.

Machine artifacts (for example `.nlc/interview-packet.json` with `goals`, `requirements`, `knowledge_domains`) are **agent-written records** of extracted goal and policy, not a third human input type.

## Consequences

- [`docs/nlc/compiler/INTENT-SURFACE.md`](../docs/nlc/compiler/INTENT-SURFACE.md) and [`docs/nlc/compiler/MANIFESTO.md`](../docs/nlc/compiler/MANIFESTO.md) state goal + policy only.
- [`/interview`](../docs/TERMS.md#interview) skill gate forbids collecting derived artifacts from the human.
- v1 binder: [`tools/fitness-nlc-0036-inference-only.py`](../tools/fitness-nlc-0036-inference-only.py) + [`rules/nlc-0036.json`](../rules/nlc-0036.json).

## Related

- [ADR 0017](0017-human-command-surface.md), [ADR 0018](0018-human-cli-interview-on-gap.md)
- [ADR 0027](0027-emit-from-prose.md) (prose → JSON; separate concern)
