from fastapi import FastAPI
from .routers import auth, emissions
from .database import engine
from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(emissions.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
