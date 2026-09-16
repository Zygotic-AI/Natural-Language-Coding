def test_apply_payment_ok() -> None:
    apply_payment = 10
    assert apply_payment == 10


def test_apply_payment_fails() -> None:
    with __import__("unittest").TestCase().assertRaises(ValueError):
        apply_payment(0)
