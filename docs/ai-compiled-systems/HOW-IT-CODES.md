# How it codes (under the covers)

Consumer-facing story: [manifesto](MANIFESTO.md) and [intent surface](INTENT-SURFACE.md). This page is **how the AI system compiler builds software** without asking humans to author noun files.

BBA/BBP shape is internal vocabulary: small boundaries, noun inside, verbs on the edge, goals only call verbs ([`CHARTER.md`](../../CHARTER.md)). You do not need that vocabulary to **use** NLC; you need it to **audit** emit.

## Pipeline (one compile)

```text
┌─────────────────────────────────────────────────────────────┐
│ Human intent (touch + approve)                               │
│   goals · requirements · knowledge domains · ADRs · adopted rules │
└────────────────────────────┬────────────────────────────────┘
                             │ PLANIT: load → interview → plan
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Bind every statement to requirement / ADR / rule ids + BBP   │
│ Close gaps (no unbound business statements)                  │
└────────────────────────────┬────────────────────────────────┘
                             │ generate ONE artifact per step
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Compiler emit: noun · verbs · adjectives · goal body · tests │
│ Tags/primitives applied per adopted if/thens (ADR 0007)      │
└────────────────────────────┬────────────────────────────────┘
                             │ immediate gate (6.5)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Machine metrics + adversarial audit on that artifact         │
│ FAIL → RCA → intent/bind → regenerate (not patch emit)       │
└────────────────────────────┬────────────────────────────────┘
                             │ prove (full tree)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Compile green · optional human release (`Released-by:`)      │
└─────────────────────────────────────────────────────────────┘
```

## What gets built when

| Step | Compiler output | Rule |
| ---- | --------------- | ---- |
| New domain concept | **Noun** + **adjectives** + **verbs** on the boundary | One home per adjective (R24 / C19) |
| Use case | **Goal** implementation | Calls verbs only; no noun field writes (R5) |
| Policy / standard adopted | **Rules** + **tags** on IR | Prose ADR → if/then; compiler applies or fails |
| Verb interior | Calls to closed **primitives** | Undeclared primitive in body → fail (ADR 0009) |
| Neighbor access | **Contracts** only | No reaching into another noun’s fields |

TypeScript or Python is an **object file**—proof that intent compiled—not the SSOT ([`COMPILER.md`](COMPILER.md)).

## When generation is incomplete

Generation stops (gate red) if any of these hold—non-exhaustive; see [`COMPILER.md`](COMPILER.md):

- Goal assigns a noun field.
- Same adjective implemented twice.
- Plan statement has no binding.
- Published verb contract broke and callers were not in the plan.
- Public boundary missing failure mode.

Same inputs + same standard → same **shape and contracts**. Interiors may change behind a contract.

## Audits in the build, not after QA

Traditional flow often finds forked business rules in UAT or production. NLC inserts **audit immediately after each emit** so the expensive stages (PR review, QA, UAT, user) see fewer novel defects. Cost model: [`QUALITY-PROCESSES.md`](QUALITY-PROCESSES.md).

## Roles (compressed)

| Role | Holds |
| ---- | ----- |
| Human manager | Goals, requirements, knowledge domains; adopts ADRs and rules; release |
| AI compiler | Nouns, verbs, adjectives, goal bodies, tests, derived views |
| Red gate | Machine signal for RCA—not a human editing the object file |

Full matrix: [`INTENT-SURFACE.md`](INTENT-SURFACE.md). Step list: [`PROCESS.md`](PROCESS.md). Orchestration in Cursor: [`PLANIT-ORCHESTRATION.md`](PLANIT-ORCHESTRATION.md).
