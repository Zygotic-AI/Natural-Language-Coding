"""DELIBERATE VIOLATION: goal copies the void adjective and the money math."""


def record_bank_payment(invoice, amount: int) -> None:
    if invoice.status == "void":
        raise ValueError("cannot pay a void invoice")
    if invoice.balance - amount < 0:
        raise ValueError("overpay")
    invoice.apply_payment(amount)
