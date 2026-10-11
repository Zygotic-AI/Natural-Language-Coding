"""DELIBERATE VIOLATION: setattr() field write bypass."""


def record_bank_payment(invoice, amount: int) -> None:
    setattr(invoice, "status", "paid")
    setattr(invoice, "balance", 0)
