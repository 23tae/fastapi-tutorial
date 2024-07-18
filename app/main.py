from fastapi import FastAPI
from .routers import auth, emissions, user
from .database import engine
from .models import Base
from .scheduler import start_scheduler
import os
from dotenv import load_dotenv


load_dotenv()

server_port = os.getenv("SERVER_PORT")

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(emissions.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    start_scheduler()
    uvicorn.run(app, port=server_port)
