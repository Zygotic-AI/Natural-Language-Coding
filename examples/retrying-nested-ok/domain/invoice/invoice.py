class Invoice:
    def __init__(self) -> None:
        self.balance = 0
        self._seen: set[str] = set()

    def apply_payment(self, amount: int, idempotency_key: str = "") -> None:
        if idempotency_key in self._seen:
            return
        self._seen.add(idempotency_key)
        self.balance = self.balance - amount
