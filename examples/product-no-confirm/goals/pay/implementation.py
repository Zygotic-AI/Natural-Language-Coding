def pay(invoice, amount: int) -> None:
    invoice.apply_payment(amount)
