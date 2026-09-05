"""Goal: record a bank payment by calling the noun verb only."""


def record_bank_payment(invoice, amount: int) -> None:
    invoice.apply_payment(amount)
