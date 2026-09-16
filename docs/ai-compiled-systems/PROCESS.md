# PLANIT: load → prove

The ACS loop. BBP is bound on every statement by default.

Fail at prove → RCA into interview or bind, then regenerate. Humans do not patch generated files to silence an audit.

## 0. Load what already exists

BBP standard (`CHARTER.md`), ADRs, requirements, known boundaries, known verb contracts. Do not interview for facts already bound.

## 1. Interview

Outcome, not feature. Stop when goals and constraints can be named. Incomplete interview → no plan.

The window stays small later because this step names the objects. A poor interview creates two Invoices. Call knowledge-steward `load-shelf` / `flag-gap` before generate; new facts wait for the manager (`propose-fact`).


## 2. Plan

Work items only, not an essay. Each item is one of:

- new/changed **goal**
- new/changed **boundary** (noun + verbs)
- new/changed **requirement** or **ADR**
- new/changed **rule** (tags / primitives / if-then; [ADR 0007](../../adrs/0007-tags-primitives-reduced-adrs.md))

If the plan cannot say which, it is not a plan. A standard that never becomes a rule is not done.


## 3. Product statements

Split the plan into single-step statements one boundary can finish.

Good: `Invoice` verbs `issue`, `applyPayment`, `void`.
Good: Goal `RecordBankPayment` calls `applyPayment` only.
Bad: “Build billing.”

## 4. Bind

Every statement points at:

- requirement ids
- ADR ids
- **rule** ids when the statement is data-policy or runtime (ADR 0007)
- the **BBP standard** (always on)


No pointer → unbound. A statement with only “BBP” and no business requirement may still be valid (pure shape work). A business statement with no requirement/ADR and no explicit “none needed, reason X” is unbound.

## 5. Close gaps

Unbound or ambiguous → question → new or clearer requirement, ADR, or knowledge-shelf fact. Loop until every statement is bound. Do not generate yet.

## 6. Generate

**Before:** the plan already names measurable criteria for *this* artifact (fitness command, charter rows, skill Gate table). No metrics → do not generate ([ADR 0010](../../adrs/0010-gate-after-every-generate.md)).

AI emits **one** statement / one artifact (one boundary, or one skill file). BBP-shaped. Neighbors only through hard contracts.

Primitive work inside a verb is calls to [`integrity/primitives.md`](../../integrity/primitives.md) functions, not raw I/O ([ADR 0009](../../adrs/0009-primitive-interior-functions.md)).

Humans do not edit the output to help.

## 6.5 Gate that artifact (mandatory)

Immediately. Default-closed. Default fail. Run the metrics named in the plan. Missing evidence = FAIL.

**FAIL** → stop. RCA to interview or bind. Do not start the next statement.

**PASS** → only then the next statement.

This applies to code, skills, prompts, and docs PLANIT emits, and to anything PLANIT is later used to create.

## 7. Prove


Both required. This is **compile**, not ship.

1. **Machine gate** — hub: `bash tools/ci-fitness.sh` (full confirmer suite, not “check 1 only”). Adopter: the fitness suite that tree bound. Exit non-zero = fail.
2. **Adversarial audit** — a different pass than the generator: statements done, bound reqs/ADRs/rules held, no second copy of an adjective inside a goal.

Fail → step 1 or 5, then step 6 again.

**Ship** is after prove and after a human writes `Released-by:` (and `Ratified-by:` when class A/B/D/E/F): `python3 tools/release-audit.py <tree>`. Prove PASS is not a release.


## Roles

| Who | Holds |
|-----|--------|
| Human | Goals, requirements, ADRs, RCA sign-off, accepted audit findings |
| AI | Nouns, verbs, goal bodies, other derived artifacts |

The red gate is not a human in the file. It is the signal RCA gets before users do.

Breaking a published verb contract is loud in that same way: prove stays red until the requirement/ADR is accepted and generated callers are in the plan ([ADR 0006](../../adrs/0006-contract-change-notice.md)). Additive contract changes are quiet (impact graph in the packet, no extra sign-off).

## Agent orchestration

Agents run this loop through the **`planit`** skill ([`.agents/skills/planit/SKILL.md`](../../.agents/skills/planit/SKILL.md)), which overlays **audited work loop (AWL)** gates and verdicts on these steps. Map, tiers, and leaf routing: [`PLANIT-ORCHESTRATION.md`](PLANIT-ORCHESTRATION.md).

