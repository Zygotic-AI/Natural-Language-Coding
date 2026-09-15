"""DELIBERATE VIOLATION (R5 only): assign noun fields. No money math."""


def record_bank_payment(invoice, amount: int) -> None:
    invoice.status = "paid"
    invoice.balance = 0
