class Invoice:
    def __init__(self, invoice_id: str) -> None:
        self.id = invoice_id
        self.status = "draft"
        self.balance = 0
