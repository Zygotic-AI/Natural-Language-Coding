"""DELIBERATE VIOLATION: mutate through __dict__ instead of apply_payment."""


def record_bank_payment(invoice, amount: int) -> None:
    state = invoice.__dict__
    apply_bank_delta(state, amount)
