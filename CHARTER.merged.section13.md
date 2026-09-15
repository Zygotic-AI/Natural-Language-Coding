> **TODO (vocabulary):** "invariant" / "laws" → **adjective** throughout. Not applied in this pass; dedicated rename pass pending.
> **TODO (binder → gate):** "binder" as a noun is retired. **Binding** = planning act; **gate** = post-generation verification. Not applied here.
> **TODO (workflow-as-peer):** workflow listed as a peer. ACS: workflow is a goal-of-goals. Confirm before §4.4 / §5.5.

## 13. Mapping to things that already exist

Use these; do not reimplement them under new folder names.

| Need | Existing tool or pattern |
|---|---|
| Noun + invariant-preserving verbs | DDD aggregate; methods or typed commands on the aggregate |
| Typed mutation contracts on the noun | Axon commands; Orleans / actor grain interface; Design by Contract |
| Goal as use-case folder | Vertical slice; Clean Architecture handler / MediatR command |
| Module privacy enforced in CI | Spring Modulith, ArchUnit, ESLint boundaries, import-linter |
| Contract schemas | Zod, TypeBox, JSON Schema, OpenAPI |
| Multi-noun time / compensation | Temporal, durable workflows |
| Generated impact / dependency | madge, dependency-cruiser, jscpd |

---

**ACS addition.** Those tools are the *compile target*, not the source. Intent — goals, requirements, ADRs — is the source; the compiler emits BBA-shaped code that those tools then enforce. Module privacy enforced in CI is check 1. Drift as a merge failure is the gate family. The charter's claim — if a rule cannot be checked, it is not a rule yet — is now the compile gate's claim too.
