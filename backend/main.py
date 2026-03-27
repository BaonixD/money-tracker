from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    # таблицы теперь управляются через: alembic -c backend/alembic.ini upgrade head
    yield

app = FastAPI(title="Money Tracker", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для прода заменить на конкретный домен фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(transaction_router)

@app.get("/")
def read_root():
    return {"Salamaleikum": "ualeikumsalaam"}

