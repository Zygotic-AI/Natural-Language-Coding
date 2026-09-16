"""Invoice noun: private-looking state; verbs are the only mutation path."""


class Invoice:
    def __init__(self, invoice_id: str) -> None:
        self.id = invoice_id
        self.status = "draft"
        self.balance = 0

    def issue(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("amount")
        if self.status != "draft":
            raise ValueError("status")
        self.status = "open"
        self.balance = amount

    def apply_payment(self, amount: int) -> None:
        if self.status != "open":
            raise ValueError("status")
        if amount <= 0:
            raise ValueError("amount")
        self.balance = self.balance - amount
        if self.balance <= 0:
            self.status = "paid"

    def void(self) -> None:
        if self.status not in ("open", "draft"):
            raise ValueError("status")
        self.status = "void"
        self.balance = 0
