"""DELIBERATE VIOLATION: multi-line attribute assignment bypass."""


def record_bank_payment(invoice, amount: int) -> None:
    (
        invoice
    ).status = "paid"
    (
        invoice
    ).balance = 0
