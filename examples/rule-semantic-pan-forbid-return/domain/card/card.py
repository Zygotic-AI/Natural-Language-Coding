"""Card noun. get_number is the one-boundary hop."""


class Card:
    def __init__(self, card_number: str) -> None:
        self.card_number = card_number

    def get_number(self) -> str:
        return self.card_number
