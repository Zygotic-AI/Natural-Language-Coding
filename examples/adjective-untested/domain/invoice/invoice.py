class Invoice:
    def __init__(self) -> None:
        self.status = "draft"

    def void(self) -> None:
        self.status = "void"
