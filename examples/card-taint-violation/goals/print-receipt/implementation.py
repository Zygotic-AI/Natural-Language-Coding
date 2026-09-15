"""DELIBERATE VIOLATION: taint leaves the consuming goal via return."""


def print_receipt(card) -> str:
    card_number = card.get_number()
    return card_number
