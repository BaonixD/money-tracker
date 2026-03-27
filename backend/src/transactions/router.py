from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.src.auth.dependencies import get_current_user
from backend.src.auth.model import User
from backend.src.transactions.schemas import TransactionCreate, TransactionResponse
from backend.src.transactions.service import create_transaction, get_transactions, get_transaction_by_id

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/create", response_model=TransactionResponse)
async def create_transaction_endpoint(
    data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        transaction = await create_transaction(db, current_user.id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return transaction


@router.get("/", response_model=list[TransactionResponse])
async def get_transactions_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_transactions(db, current_user.id)


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_endpoint(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = await get_transaction_by_id(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return transaction
