class Invoice:
    def apply_payment(self, amount: str) -> None:
        self.balance = amount
