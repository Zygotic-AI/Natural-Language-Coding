"""DELIBERATE VIOLATION: goal writes noun fields instead of calling apply_payment."""


def record_bank_payment(invoice, amount: int) -> None:
    invoice.balance = invoice.balance - amount
    invoice.status = "paid"
