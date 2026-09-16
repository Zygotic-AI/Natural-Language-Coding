from helpers.money import format_money


def refund(invoice, amount: int) -> None:
    invoice.apply_payment(-amount)
    format_money(amount)
