from fastapi import APIRouter, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.database import db
import uuid

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
    try:
        # Log the incoming data
        print("\n=== Invoice Creation Debug ===")
        print(f"Received invoice data: {invoice.dict()}")
        print(f"Client name: {invoice.clientName}")
        print(f"Description: {invoice.description}")
        print(f"Amount: {invoice.amount}")
        print(f"Due date: {invoice.dueDate}")
        print(f"Issued at: {invoice.issuedAt}")
        print(f"Paid: {invoice.paid}")
        print(f"Task IDs: {invoice.taskIds}")
        print("=== End of Received Data ===\n")
        
        # Convert the dates to datetime objects
        issued_at = invoice.issuedAt or datetime.now()
        due_date = invoice.dueDate

        # Prepare the data for Prisma
        invoice_data = {
            "invoiceNumber": invoice.invoiceNumber,
            "clientName": invoice.clientName,
            "description": invoice.description,
            "amount": invoice.amount,
            "issuedAt": issued_at,
            "dueDate": due_date,
            "paid": invoice.paid,
            "tasks": {
                "connect": [{"id": task_id} for task_id in invoice.taskIds] if invoice.taskIds else []
            }
        }
        
        # Log the data being sent to Prisma
        print("\n=== Prisma Data Debug ===")
        print(f"Sending to Prisma: {invoice_data}")
        print(f"Invoice number to Prisma: {invoice_data['invoiceNumber']}")
        print(f"Client name to Prisma: {invoice_data['clientName']}")
        print(f"Description to Prisma: {invoice_data['description']}")
        print(f"Amount to Prisma: {invoice_data['amount']}")
        print(f"Due date to Prisma: {invoice_data['dueDate']}")
        print(f"Issued at to Prisma: {invoice_data['issuedAt']}")
        print(f"Paid to Prisma: {invoice_data['paid']}")
        print(f"Tasks to Prisma: {invoice_data['tasks']}")
        print("=== End of Prisma Data ===\n")

        # Create the invoice using Prisma
        created_invoice = await db.invoice.create(data=invoice_data)
        
        # Convert the result to a dictionary
        invoice_dict = {
            "id": created_invoice.id,
            "invoiceNumber": created_invoice.invoiceNumber,
            "clientName": created_invoice.clientName,
            "description": created_invoice.description,
            "amount": created_invoice.amount,
            "issuedAt": created_invoice.issuedAt,
            "dueDate": created_invoice.dueDate,
            "paid": created_invoice.paid,
            "tasks": created_invoice.tasks
        }
        
        return invoice_dict
    except Exception as e:
        print(f"\n=== Error Debug ===")
        print(f"Error creating invoice: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error details: {e.__dict__}")
        print("=== End of Error ===\n")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int):
    invoice = await db.invoice.find_unique(
        where={"id": invoice_id},
        include={"tasks": True}  # Include tasks if you want
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
