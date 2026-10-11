"""DELIBERATE VIOLATION: object.__setattr__ field write bypass."""


def record_bank_payment(invoice, amount: int) -> None:
    object.__setattr__(invoice, "status", "paid")
    object.__setattr__(invoice, "balance", 0)
