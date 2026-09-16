"""Broken on purpose: names apply_payment, never a failure path."""


def test_apply_payment_reduces_balance() -> None:
    balance = 50
    apply_payment = balance - 20
    assert apply_payment == 30
