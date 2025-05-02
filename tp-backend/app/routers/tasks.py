from fastapi import APIRouter, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from app.database import db

router = APIRouter()

class TaskIn(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

@router.post("/tasks/")
async def create_task(task: TaskIn):
    return await db.task.create(task.dict())

@router.get("/tasks/")
async def get_tasks():
    return await db.task.find_many()

@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = await db.task.find_unique(where={"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskIn):
    updated = await db.task.update(
        where={"id": task_id},
        data=task.dict()
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    deleted = await db.task.delete(where={"id": task_id})
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}