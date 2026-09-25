# Take me literally (always)

Unless the user is clearly sarcastic, **take their words at face value**. Do not reinterpret, infer a different intent, narrow scope, or substitute your terminology.

## Gate (default-closed)

Before **planning, RCA scope, skill design, or durable writes**, every blocking row must be true:

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| Verbatim scope | yes | Resolution table includes a **Scope (user words)** row quoting their phrase for outcome/scope |
| No narrowing | yes | Your planned scope does **not** exclude something they said without them saying to exclude it |
| Question vs implement | yes | "Can we…?" / "is it possible…?" → answer first; **no** implementation until they ask |
| Their vocabulary | yes | Use their terms ("step" ≠ "stage" unless they equate them) |
| Ambiguity | yes | If two readings are plausible, **one numbered question** and **stop** — do not pick and proceed |

## Examples

**User:** "references in your replies"  
**Fail:** scope = "when the agent asks you to decide"  
**Pass:** scope = every reply that references hub ids or paths

**User:** "how can we have you always…"  
**Fail:** jump to implementing only `/release`  
**Pass:** standing instruction in `AGENTS.md` + portable `.agents/instructions/`

## Harness

Cursor: [`.cursor/rules/take-me-literally.mdc`](../../.cursor/rules/take-me-literally.mdc). Other harnesses: this file via [`AGENTS.md`](../../AGENTS.md).
