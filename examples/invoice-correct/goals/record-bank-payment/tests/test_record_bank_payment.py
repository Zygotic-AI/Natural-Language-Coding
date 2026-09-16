"""Use-case test: the goal calls the noun verb. Does not re-assert adjectives."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from implementation import record_bank_payment  # noqa: E402


def test_records_bank_payment_calls_apply_payment() -> None:
    called: list[int] = []

    class Invoice:
        def apply_payment(self, amount: int) -> None:
            called.append(amount)

    record_bank_payment(Invoice(), 25)
    assert called == [25]
