def pay(cursor, invoice_id: str) -> None:
    cursor.execute("UPDATE invoice SET status = %s WHERE id = %s", ("paid", invoice_id))
