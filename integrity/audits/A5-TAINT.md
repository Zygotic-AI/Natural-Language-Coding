# A5 — taint lifetime / one boundary (v1)

Not a binding-matrix id. Adversarial-audit concern.

## Statement

A tainted adjective (card number, PAN, SSN, name-when-PII) may cross **one** boundary: the consuming verb. It must not be returned from that unit or stored on another object.

## V1 gate

`tools/fitness-taint-lifetime.py`

Tokens: `domain/<noun>/taint.txt`.
Fails: `return … card_number`, `other.field = card_number` in goals/adapters.
Does not fail: local use after `card.get_number()`.

Known-fail: `examples/card-taint-violation/`.

## Not bound

No matrix row. V1 does not track locals across lines or gateway calls.
