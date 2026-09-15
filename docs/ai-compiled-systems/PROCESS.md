# Process: load → prove

The AI-Compiled Systems loop. BBA is bound on every statement by default.

Fail at prove → RCA into interview or bind, then regenerate. Humans do not patch generated files to silence an audit.

## 0. Load what already exists

BBA standard (`CHARTER.md`), ADRs, requirements, known boundaries, known verb contracts. Do not interview for facts already bound.

## 1. Interview

Outcome, not feature. Stop when goals and constraints can be named. Incomplete interview → no plan.

The window stays small later because this step names the objects. A poor interview creates two Invoices.

## 2. Plan

Work items only, not an essay. Each item is one of:

- new/changed **goal**
- new/changed **boundary** (noun + verbs)
- new/changed **requirement** or **ADR**

If the plan cannot say which, it is not a plan.

## 3. Product statements

Split the plan into single-step statements one boundary can finish.

Good: `Invoice` verbs `issue`, `applyPayment`, `void`.
Good: Goal `RecordBankPayment` calls `applyPayment` only.
Bad: “Build billing.”

## 4. Bind

Every statement points at:

- requirement ids
- ADR ids
- the **BBA standard** (always on)

No pointer → unbound. A statement with only “BBA” and no business requirement may still be valid (pure shape work). A business statement with no requirement/ADR and no explicit “none needed, reason X” is unbound.

## 5. Close gaps

Unbound or ambiguous → question → new or clearer requirement, ADR, or knowledge-shelf fact. Loop until every statement is bound. Do not generate yet.

## 6. Generate

AI emits BBA-shaped code for those statements only.

Inside a boundary: self-contained. Neighbors only through hard contracts. The write window is that object plus the contracts it is allowed to call.

Humans do not edit the output to help.

## 7. Prove

Both required:

1. **Machine binder** — at least check 1 (no goal writes noun fields). Exit non-zero = fail.
2. **Adversarial audit** — a different pass than the generator: statements done, bound reqs/ADRs held, no second copy of an invariant inside a goal.

Fail → step 1 or 5, then step 6 again.

## Roles

| Who | Holds |
|-----|--------|
| Human | Goals, requirements, ADRs, RCA sign-off, accepted audit findings |
| AI | Nouns, verbs, goal bodies, other derived artifacts |

The red binder is not a human in the file. It is the signal RCA gets before users do.
