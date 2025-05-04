from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import HourEntry as HourEntryModel
from app.schemas.task import HourEntryCreate, HourEntryRead, HourEntryUpdate

router = APIRouter(prefix="/hour-entries", tags=["hour-entries"])


@router.post("/", response_model=HourEntryRead)
def create_hour_entry(
    entry_in: HourEntryCreate,
    db: Session = Depends(get_db)
):
    db_entry = HourEntryModel(
        task_id=entry_in.task_id,
        date=entry_in.date,
        hours=entry_in.hours,
        notes=entry_in.notes,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/", response_model=List[HourEntryRead])
def get_hour_entries(db: Session = Depends(get_db)):
    return db.query(HourEntryModel).all()


@router.get("/{entry_id}", response_model=HourEntryRead)
def get_hour_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(HourEntryModel).get(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="HourEntry not found")
    return entry


@router.put("/{entry_id}", response_model=HourEntryRead)
def update_hour_entry(
    entry_id: int,
    entry_in: HourEntryUpdate,
    db: Session = Depends(get_db)
):
    entry = db.query(HourEntryModel).get(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="HourEntry not found")

    for field, value in entry_in.dict(exclude_unset=True).items():
        setattr(entry, field, value)

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", response_model=dict)
def delete_hour_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(HourEntryModel).get(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="HourEntry not found")
    db.delete(entry)
    db.commit()
    return {"ok": True}
