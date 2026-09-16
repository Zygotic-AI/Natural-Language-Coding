def record_bank_payment(invoice, amount: int) -> None:
    for attempt in range(3):
        invoice.apply_payment(amount)
        break
