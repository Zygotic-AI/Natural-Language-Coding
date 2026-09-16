class Invoice:
    def apply_payment(self, amount: int) -> None:
        for attempt in range(3):
            self.balance = self.balance - amount
            break
