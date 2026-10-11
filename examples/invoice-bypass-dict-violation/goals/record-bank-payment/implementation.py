"""DELIBERATE VIOLATION: __dict__ field write bypass."""


def record_bank_payment(invoice, amount: int) -> None:
    invoice.__dict__["status"] = "paid"
    invoice.__dict__["balance"] = 0
