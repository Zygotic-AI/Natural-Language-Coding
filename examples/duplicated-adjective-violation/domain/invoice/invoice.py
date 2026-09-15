class Invoice:
    def void(self) -> None:
        if self.status == "void":
            return
        self.status = "void"

    def apply_payment(self, amount: int) -> None:
        self.balance = self.balance - amount
