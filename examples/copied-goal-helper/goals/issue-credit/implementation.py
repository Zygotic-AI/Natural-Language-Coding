def next_id(prefix, n):
    if n < 1:
        n = 1
    return f"{prefix}-{n}"


def issue_credit(invoice, amount: int) -> None:
    invoice.apply_payment(amount)
