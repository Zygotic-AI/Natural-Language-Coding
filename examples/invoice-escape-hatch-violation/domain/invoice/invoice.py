"""Invoice noun. Verbs exist; the goal uses __dict__ instead."""


class Invoice:
    def __init__(self, invoice_id: str) -> None:
        self.id = invoice_id
        self.status = "draft"
        self.balance = 0

    def apply_payment(self, amount: int) -> None:
        self.balance = self.balance - amount
        if self.balance <= 0:
            self.status = "paid"
