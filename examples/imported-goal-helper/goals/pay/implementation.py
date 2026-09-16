from helpers.money import format_money


def pay(invoice, amount: int) -> None:
    invoice.apply_payment(amount)
    format_money(amount)
