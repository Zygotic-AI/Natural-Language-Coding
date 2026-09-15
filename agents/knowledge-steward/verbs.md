# Knowledge Steward — Verbs

Each verb has input, output, and failure mode.

## load-shelf

Query. Return confirmed facts for a scope. Does not grant write authority.

### Input contract

```yaml
input:
  required: [scope]
  properties:
    scope:
      type: string
      description: Topic or noun id (e.g. invoice, pii)
    include_proposals:
      type: boolean
      default: false
```

### Output contract

```yaml
output:
  required: [status, facts]
  properties:
    status:
      enum: [loaded, empty, error]
    facts:
      type: array
      items:
        type: object
        required: [id, statement, status]
```

### Failure mode

```yaml
error:
  required: [code, message]
  properties:
    code:
      enum: [INVALID_SCOPE, SHELF_UNAVAILABLE]
```

## propose-fact

Draft a fact card. Status is `needs_confirm` until a human manager accepts it.

### Input contract

```yaml
input:
  required: [statement, rationale]
  properties:
    statement:
      type: string
    rationale:
      type: string
    related_nouns:
      type: array
      items:
        type: string
```

### Output contract

```yaml
output:
  required: [path, status]
  properties:
    path:
      type: string
    status:
      enum: [needs_confirm]
```

### Failure mode

```yaml
error:
  required: [code, message]
  properties:
    code:
      enum: [MISSING_STATEMENT, DUPLICATE_FACT, LOOKS_LIKE_A_RULE]
```

`LOOKS_LIKE_A_RULE` — the text is an R*/C* in disguise. Send it to standards-steward.

## flag-gap

Name a product statement with no fact, requirement, or ADR.

### Input contract

```yaml
input:
  required: [statement_id, question]
  properties:
    statement_id:
      type: string
    question:
      type: string
```

### Output contract

```yaml
output:
  required: [gap_id, status]
  properties:
    gap_id:
      type: string
    status:
      enum: [open]
```

### Failure mode

```yaml
error:
  required: [code, message]
  properties:
    code:
      enum: [MISSING_QUESTION, ALREADY_BOUND]
```

## Excluded verbs

No `ratify`, `merge`, `release`, `approve`.
