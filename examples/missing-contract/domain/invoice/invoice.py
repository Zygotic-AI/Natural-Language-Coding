class Invoice:
    def apply_payment(self, amount: int) -> None:
        self.balance = getattr(self, "balance", 0) - amount
