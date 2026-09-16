class Invoice:
    def apply_payment(self, amount: int) -> None:
        self.balance = self.balance - amount
