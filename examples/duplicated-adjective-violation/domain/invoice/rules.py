def already_void(invoice) -> bool:
    return invoice.status == "void"
