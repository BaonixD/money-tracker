from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.src.auth.dependencies import get_current_user
from backend.src.auth.model import User
from backend.src.transactions.schemas import (
    TransactionCreate, TransactionResponse, TransactionUpdate,
    StatisticsResponse, PaginatedResponse,
)
from backend.src.transactions.service import (
    create_transaction, get_transactions, get_transaction_by_id,
    update_transaction, delete_transaction, get_statistics, count_transactions,
)

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


@router.get("/stats", response_model=StatisticsResponse)
async def get_statistics_endpoint(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_statistics(db, current_user.id, date_from, date_to)


@router.get("/", response_model=PaginatedResponse)
async def get_transactions_endpoint(
    category_id: int | None = None,
    type: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = await get_transactions(
        db, current_user.id,
        category_id=category_id, type=type,
        date_from=date_from, date_to=date_to,
        limit=limit, offset=offset,
    )
    total = await count_transactions(
        db, current_user.id,
        category_id=category_id, type=type,
        date_from=date_from, date_to=date_to,
    )
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


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


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction_endpoint(
    transaction_id: int,
    data: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        transaction = await update_transaction(db, transaction_id, current_user.id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return transaction


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction_endpoint(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = await delete_transaction(db, transaction_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
