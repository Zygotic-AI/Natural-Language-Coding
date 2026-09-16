def record_bank_payment(invoice, amount: int, key: str) -> None:
    for attempt in range(3):
        invoice.apply_payment(amount, idempotency_key=key)
        break
