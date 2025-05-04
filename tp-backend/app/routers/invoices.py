from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Invoice as InvoiceModel, Task as TaskModel
from app.schemas.task import InvoiceCreate, InvoiceRead, InvoiceUpdate

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=InvoiceRead)
def create_invoice(
    invoice_in: InvoiceCreate,
    db: Session = Depends(get_db)
):
    issued_at = invoice_in.issued_at or datetime.utcnow()
    db_invoice = InvoiceModel(
        invoice_number=invoice_in.invoice_number,
        client_name=invoice_in.client_name,
        description=invoice_in.description,
        amount=invoice_in.amount,
        issued_at=issued_at,
        due_date=invoice_in.due_date,
        paid=invoice_in.paid,
    )

    if invoice_in.task_ids:
        tasks = db.query(TaskModel).filter(TaskModel.id.in_(invoice_in.task_ids)).all()
        db_invoice.tasks = tasks

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@router.get("/", response_model=List[InvoiceRead])
def get_invoices(db: Session = Depends(get_db)):
    return db.query(InvoiceModel).all()


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(InvoiceModel).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv


@router.put("/{invoice_id}", response_model=InvoiceRead)
def update_invoice(
    invoice_id: int,
    invoice_in: InvoiceUpdate,
    db: Session = Depends(get_db)
):
    inv = db.query(InvoiceModel).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    data = invoice_in.dict(exclude_unset=True)
    task_ids = data.pop("task_ids", None)
    for field, value in data.items():
        setattr(inv, field, value)

    if task_ids is not None:
        tasks = db.query(TaskModel).filter(TaskModel.id.in_(task_ids)).all()
        inv.tasks = tasks

    db.commit()
    db.refresh(inv)
    return inv


@router.delete("/{invoice_id}", response_model=dict)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(InvoiceModel).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(inv)
    db.commit()
    return {"ok": True}
