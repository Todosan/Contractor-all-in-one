from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import ScheduleEvent as ScheduleEventModel
from app.schemas.event import ScheduleEventCreate, ScheduleEventRead, ScheduleEventUpdate

router = APIRouter(prefix="/schedule-events", tags=["schedule-events"])

@router.post("/", response_model=ScheduleEventRead)
def create_schedule_event(
    event_in: ScheduleEventCreate,
    db: Session = Depends(get_db)
):
    db_event = ScheduleEventModel(
        title=event_in.title,
        description=event_in.description,
        start=event_in.start,
        end=event_in.end,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/", response_model=List[ScheduleEventRead])
def get_schedule_events(db: Session = Depends(get_db)):
    return db.query(ScheduleEventModel).all()


@router.get("/{event_id}", response_model=ScheduleEventRead)
def get_schedule_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(ScheduleEventModel).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="ScheduleEvent not found")
    return event


@router.put("/{event_id}", response_model=ScheduleEventRead)
def update_schedule_event(
    event_id: int,
    event_in: ScheduleEventUpdate,
    db: Session = Depends(get_db)
):
    event = db.query(ScheduleEventModel).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="ScheduleEvent not found")

    for field, value in event_in.dict(exclude_unset=True).items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}", response_model=dict)
def delete_schedule_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(ScheduleEventModel).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="ScheduleEvent not found")
    db.delete(event)
    db.commit()
    return {"ok": True}
