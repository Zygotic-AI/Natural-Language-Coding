class Invoice:
    def apply_payment(self, amount: int) -> None:
        self.balance = self.balance - amount
        self.status = "paid"

    def export_csv(self) -> str:
        return "invoice,csv"
