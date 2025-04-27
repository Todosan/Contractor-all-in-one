from fastapi import APIRouter, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.database import db

router = APIRouter()

class ScheduleEventIn(BaseModel):
    title: str
    description: Optional[str] = None
    start: datetime
    end: datetime

@router.post("/schedule-events/")
async def create_schedule_event(event: ScheduleEventIn):
    return await db.scheduleevent.create(event.dict())

@router.get("/schedule-events/")
async def get_schedule_events():
    return await db.scheduleevent.find_many()

@router.get("/schedule-events/{event_id}")
async def get_schedule_event(event_id: int):
    event = await db.scheduleevent.find_unique(where={"id": event_id})
    if not event:
        raise HTTPException(status_code=404, detail="ScheduleEvent not found")
    return event

@router.put("/schedule-events/{event_id}")
async def update_schedule_event(event_id: int, event: ScheduleEventIn):
    updated = await db.scheduleevent.update(
        where={"id": event_id},
        data=event.dict()
    )
    if not updated:
        raise HTTPException(status_code=404, detail="ScheduleEvent not found")
    return updated

@router.delete("/schedule-events/{event_id}")
async def delete_schedule_event(event_id: int):
    deleted = await db.scheduleevent.delete(where={"id": event_id})
    if not deleted:
        raise HTTPException(status_code=404, detail="ScheduleEvent not found")
    return {"ok": True}