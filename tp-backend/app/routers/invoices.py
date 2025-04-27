from fastapi import APIRouter, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.database import db

router = APIRouter()

class InvoiceIn(BaseModel):
    invoiceNumber: str
    clientName: str
    description: str
    amount: float
    issuedAt: Optional[datetime] = None
    dueDate: datetime
    paid: bool = False
    taskIds: Optional[List[int]] = None


@router.post("/invoices/")
async def create_invoice(invoice: InvoiceIn):
    invoice_data = {
        "invoiceNumber": invoice.invoiceNumber,
        "clientName": invoice.clientName,
        "description": invoice.description,
        "amount": invoice.amount,
        "issuedAt": invoice.issuedAt or datetime.now(),
        "dueDate": invoice.dueDate,
        "paid": invoice.paid,
    }

    if invoice.taskIds:
        invoice_data["tasks"] = {
            "connect": [{"id": task_id} for task_id in invoice.taskIds]
        }

    created_invoice = await db.invoice.create(data=invoice_data)
    return created_invoice

@router.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int):
    invoice = await db.invoice.find_unique(
        where={"id": invoice_id},
        include={"tasks": True}  # 👈 Include tasks if you want
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/invoices/{invoice_id}")
async def update_invoice(invoice_id: int, invoice: InvoiceIn):
    updated = await db.invoice.update(
        where={"id": invoice_id},
        data=invoice.dict(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return updated

@router.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: int):
    deleted = await db.invoice.delete(where={"id": invoice_id})
    if not deleted:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"ok": True}
