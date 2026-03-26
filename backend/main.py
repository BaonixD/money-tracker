from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.database import engine, Base
from backend.src.auth.router import router as auth_router
from backend.src.auth.model import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Money Tracker", lifespan=lifespan)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"Salamaleikum": "ualeikumsalaam"}

