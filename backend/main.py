from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.database import engine, Base
from backend.src.auth.router import router as auth_router
from backend.src.category.router import router as category_router
from backend.src.transactions.router import router as transaction_router

# импорт моделей чтобы Base.metadata их увидел при create_all
from backend.src.auth.model import User
from backend.src.category.model import Category
from backend.src.transactions.model import Transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Money Tracker", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(transaction_router)

@app.get("/")
def read_root():
    return {"Salamaleikum": "ualeikumsalaam"}

