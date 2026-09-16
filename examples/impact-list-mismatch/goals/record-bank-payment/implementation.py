def record_bank_payment(invoice, amount: int) -> None:
    invoice.apply_payment(amount)
