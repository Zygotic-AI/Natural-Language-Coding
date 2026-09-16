class Invoice:
    def apply_payment(self, amount: int, idempotency_key: str = "") -> None:
        self.balance = self.balance - amount
