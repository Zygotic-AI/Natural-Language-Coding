# billing

## Step s1: create invoice noun with issue verb
- Action a1: emit Invoice.issue [adr:0001,adr:0003]
- Action a2: emit Invoice.applyPayment [adr:0001]
## Emit e1: domain/invoice.py
  trace: chose noun Invoice per ADR 0003
  anchor: noun vs goal
## Emit e2: domain/invoice_apply_payment.py
  trace: verb applyPayment stays on Invoice noun
  anchor: no noun inheritance
