"""Noun verb tests for the invoice-correct fixture (unittest only)."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from invoice import Invoice  # noqa: E402


class TestInvoice(unittest.TestCase):
    def test_issue_sets_open_and_balance(self) -> None:
        inv = Invoice("inv-1")
        inv.issue(100)
        self.assertEqual(inv.status, "open")
        self.assertEqual(inv.balance, 100)

    def test_apply_payment_reduces_balance_and_pays_when_zero(self) -> None:
        inv = Invoice("inv-2")
        inv.issue(50)
        inv.apply_payment(20)
        self.assertEqual(inv.balance, 30)
        self.assertEqual(inv.status, "open")
        inv.apply_payment(30)
        self.assertEqual(inv.balance, 0)
        self.assertEqual(inv.status, "paid")

    def test_void_sets_void_and_zero_balance(self) -> None:
        inv = Invoice("inv-3")
        inv.issue(40)
        inv.void()
        self.assertEqual(inv.status, "void")
        self.assertEqual(inv.balance, 0)


if __name__ == "__main__":
    unittest.main()
