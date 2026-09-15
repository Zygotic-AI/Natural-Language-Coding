"""DELIBERATE VIOLATION: persist the invoice without calling apply_payment."""


def record_bank_payment(invoice, amount: int, invoice_repo, db) -> None:
    invoice_repo.save(invoice)
    db.execute("UPDATE invoices SET status = 'paid' WHERE id = %s", invoice.id)
