# [PLANIT](../TERMS.md#planit): load → [verify](../TERMS.md#verify)

The [ACS](../TERMS.md#acs) loop. [BBP](../TERMS.md#bbp) is bound on every statement by default.

Fail at [verify](../TERMS.md#verify) → [RCA](../TERMS.md#rca) into [interview](../TERMS.md#interview) or bind, then regenerate. Humans do not patch generated files to silence an [audit](../TERMS.md#audit).

## 0. Load what already exists

[BBP](../TERMS.md#bbp) standard (`CHARTER.md`), ADRs, requirements, known boundaries, known verb contracts. Do not [interview](../TERMS.md#interview) for facts already bound.

## 1. [Interview](../TERMS.md#interview)

Outcome, not feature. Stop when goals and constraints can be named. Incomplete [interview](../TERMS.md#interview) → no plan.

The window stays small later because this step names the objects. A poor [interview](../TERMS.md#interview) creates two Invoices. Call knowledge-steward `load-knowledge-domain` / `flag-gap` before generate; new facts wait for the manager (`propose-fact`).

Prompt catalog (empirical, grows from RCA): [INTERVIEW-PATTERNS.md](INTERVIEW-PATTERNS.md).


## 2. Plan

Work items only, not an essay. Each item is one of:

- new/changed **[goal](../TERMS.md#goal)**
- new/changed **[boundary](../TERMS.md#boundary)** (noun + verbs)
- new/changed **[requirement](../TERMS.md#requirement)** or **[ADR](../TERMS.md#adr)**
- new/changed **[rule](../TERMS.md#rule)** (tags / primitives / if-then; [ADR 0007](../../adrs/0007-tags-primitives-reduced-adrs.md))

If the plan cannot say which, it is not a plan. A standard that never becomes a [rule](../TERMS.md#rule) is not done.

Decompose the plan into **atomic actions** (ADR 0024): each action has `id`, `plan_step_id`, `description`. Before any emit, **X1** validates every action maps to a plan step and every step has an action; **X2** confirms every applicable ADR is bound to an action. Both run through `tools/nlc-pipeline-wire.py` (ADR 0030).

## 3. Product statements

Split the plan into single-step statements one **[boundary](../TERMS.md#boundary)** can finish.

Good: `Invoice` verbs `issue`, `applyPayment`, `void`.
Good: [Goal](../TERMS.md#goal) `RecordBankPayment` calls `applyPayment` only.
Bad: “Build billing.”

## 4. Bind

Every statement points at:

- [requirement](../TERMS.md#requirement) ids
- [ADR](../TERMS.md#adr) ids
- **[rule](../TERMS.md#rule)** ids when the statement is data-policy or runtime (ADR 0007)
- the **[BBP](../TERMS.md#bbp) standard** (always on)


No pointer → unbound. A statement with only “[BBP](../TERMS.md#bbp)” and no business [requirement](../TERMS.md#requirement) may still be valid (pure shape work). A business statement with no requirement/ADR and no explicit “none needed, reason X” is unbound.

## 5. Close gaps

Unbound or ambiguous → question → new or clearer [requirement](../TERMS.md#requirement), [ADR](../TERMS.md#adr), or knowledge-domain fact. Loop until every statement is bound. Do not generate yet.

## 6. Generate

**Before:** the plan already names measurable criteria for *this* artifact (fitness command, charter rows, skill Gate table). No metrics → do not generate ([ADR 0010](../../adrs/0010-gate-after-every-generate.md)).

AI emits **one** statement / one artifact (one boundary, or one skill file). BBP-shaped. Neighbors only through hard contracts.

[Primitive](../TERMS.md#primitive) work inside a verb is calls to [`integrity/primitives.md`](../../integrity/primitives.md) functions, not raw I/O ([ADR 0009](../../adrs/0009-primitive-interior-functions.md)).

Humans do not edit the output to help.

**After emit:** write `emit-manifest.json` beside the artifact (schema [`docs/nlc/emit-manifest.schema.json`](../nlc/emit-manifest.schema.json)). Re-run the pipeline wire: **X5** (every emit has an audit), **X3** (manifest schema, `unused=na`, gate closed), **X6** (gates of ADRs bound to this action). FAIL → stop.

## 6.5 [Gate](../TERMS.md#gate) that artifact (mandatory)

Immediately. [Default-closed](../TERMS.md#default-closed). Default fail. Run the metrics named in the plan. Missing evidence = FAIL.

**FAIL** → stop. [RCA](../TERMS.md#rca) to [interview](../TERMS.md#interview) or bind. Do not start the next statement.

**PASS** → only then the next statement.

This applies to code, skills, prompts, and docs [PLANIT](../TERMS.md#planit) emits, and to anything [PLANIT](../TERMS.md#planit) is later used to create.

## 7. [Verify](../TERMS.md#verify)


Both required. This is **compile**, not [ship](../TERMS.md#ship). [Adopter](../TERMS.md#adopter) shell: `./nlc verify` (fast) and `./nlc verify-deep` (full gates + fingerprints).

1. **Machine [gate](../TERMS.md#gate)** — [hub](../TERMS.md#hub): `python3 tools/ci_fitness.py` (full confirmer suite, not “check 1 only”). [Adopter](../TERMS.md#adopter): `release-audit` and/or `.nlc/verify-suite.json` ([`APP-VERIFY.md`](../nlc/APP-VERIFY.md)). Exit non-zero = fail.
2. **Adversarial [audit](../TERMS.md#audit)** — a different pass than the generator: statements done, bound reqs/ADRs/rules held, no second copy of an [adjective](../TERMS.md#adjective) inside a [goal](../TERMS.md#goal). Human judgment gates: [`HUMAN-JUDGMENT-GATES.md`](../nlc/HUMAN-JUDGMENT-GATES.md).

Fail → step 1 or 5, then step 6 again.

**[Ship](../TERMS.md#ship)** is after [verify](../TERMS.md#verify) and after a human writes `Released-by:` (and `Ratified-by:` when class A/B/D/E/F): `python3 tools/release-audit.py <tree>` or `./nlc ship-check`. [Verify](../TERMS.md#verify) PASS is not a release.


## Roles

| Who | Holds |
|-----|--------|
| Human | Goals, requirements, ADRs, [RCA](../TERMS.md#rca) sign-off, accepted [audit](../TERMS.md#audit) findings |
| AI | Nouns, verbs, [goal](../TERMS.md#goal) bodies, other derived artifacts |

The red [gate](../TERMS.md#gate) is not a human in the file. It is the signal [RCA](../TERMS.md#rca) gets before users do.

Breaking a [published verb contract](../TERMS.md#published-verb-contract) is loud in that same way: [verify](../TERMS.md#verify) stays red until the requirement/ADR is accepted and generated callers are in the plan ([ADR 0006](../../adrs/0006-contract-change-notice.md)). Additive [contract](../TERMS.md#contract) changes are quiet (impact graph in the packet, no extra sign-off).

## Agent orchestration

Agents run this loop through the **`planit`** skill ([`.agents/skills/planit/SKILL.md`](../../.agents/skills/planit/SKILL.md)), which overlays **audited work loop (AWL)** gates and verdicts on these steps. Map, tiers, and leaf routing: [`PLANIT-ORCHESTRATION.md`](PLANIT-ORCHESTRATION.md).

