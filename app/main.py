from fastapi import FastAPI
from .routers import auth, emissions, user
from .database import engine
from .models import Base
from .scheduler import start_scheduler
import asyncio

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(emissions.router)
app.include_router(user.router)


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_scheduler())


@app.get("/")
async def root():
    return {"message": "Hello World"}
