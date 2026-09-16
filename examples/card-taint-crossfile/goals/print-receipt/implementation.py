from helper import leak


def print_receipt(card) -> str:
    return leak(card)
