class Document:
    def __init__(self) -> None:
        self.status = "draft"


class Invoice(Document):
    def apply_payment(self, amount: int) -> None:
        pass
