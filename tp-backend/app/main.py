from fastapi import FastAPI
from prisma import Prisma
from app.routers import tasks, invoices, hour_entries, schedule_events
from app.database import db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

app.include_router(tasks.router)
app.include_router(invoices.router)
app.include_router(hour_entries.router)
app.include_router(schedule_events.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Updated to match your frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
