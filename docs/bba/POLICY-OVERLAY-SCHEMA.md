# Policy overlay schema (BBA)

Conditional rules evaluated over **(tagged datum × atomic verb)** during the BBA emit process, step 5.

## Rule shape

```
IF  datum.tag == <tag>  AND  verb == <atomic_verb>
THEN obligation = <obligation_id>
```

- `datum.tag` — an adjective attached to a noun, read as a data-type tag (e.g. `card_number`, `pii`, `encrypted`).
- `verb` — one member of the closed atomic verb set.
- `obligation` — a named, testable requirement the generated code must satisfy (e.g. `encrypt_at_rest`, `audit_log`, `rate_limit`).

## Example

```
IF  datum.tag == card_number  AND  verb == write
THEN obligation = encrypt_at_rest
```

## Gate (counterpoint to step 5)

- Every rule whose condition matches the resolved graph **fired**.
- No applicable rule was silently skipped.
- Every fired obligation is present in the step-5 manifest as a bound obligation (full schema; absent optional fields = `na`).

## Non-goals

- This schema does **not** select which rules run. Selection happens at plan time (bound ADRs → reverse audit). The overlay only **evaluates** the bound rules against the tagged graph.
- Compound verbs are forbidden upstream (step 3); the overlay never sees them.

---
_Ara · 2026-09-22_
