class Customer:
    def pay_invoice(self, invoice, amount: int) -> None:
        invoice.apply_payment(amount)
