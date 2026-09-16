def next_id(prefix, n):
    if n < 1:
        n = 1
    return f"{prefix}-{n}"


def record_bank_payment(invoice, amount: int) -> None:
    invoice.apply_payment(amount)
