from fastapi import APIRouter, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.database import db

router = APIRouter()


class HourEntryIn(BaseModel):
    taskId: Optional[int] = None
    date: datetime
    hours: float
    notes: Optional[str] = None

@router.post("/hour-entries/")
async def create_hour_entry(entry: HourEntryIn):
    return await db.hourentry.create(entry.dict())

@router.get("/hour-entries/")
async def get_hour_entries():
    return await db.hourentry.find_many()

@router.get("/hour-entries/{entry_id}")
async def get_hour_entry(entry_id: int):
    entry = await db.hourentry.find_unique(where={"id": entry_id})
    if not entry:
        raise HTTPException(status_code=404, detail="HourEntry not found")
    return entry

@router.put("/hour-entries/{entry_id}")
async def update_hour_entry(entry_id: int, entry: HourEntryIn):
    updated = await db.hourentry.update(
        where={"id": entry_id},
        data=entry.dict()
    )
    if not updated:
        raise HTTPException(status_code=404, detail="HourEntry not found")
    return updated

@router.delete("/hour-entries/{entry_id}")
async def delete_hour_entry(entry_id: int):
    deleted = await db.hourentry.delete(where={"id": entry_id})
    if not deleted:
        raise HTTPException(status_code=404, detail="HourEntry not found")
    return {"ok": True}