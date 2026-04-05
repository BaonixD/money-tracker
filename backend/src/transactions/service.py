from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.transactions.model import Transaction
from backend.src.transactions.schemas import TransactionCreate, TransactionUpdate
from backend.src.category.service import get_category_by_id


async def create_transaction(db: AsyncSession, user_id: int, data: TransactionCreate) -> Transaction:
    category = await get_category_by_id(db, data.category_id)
    if not category:
        raise ValueError("Category not found")

    transaction = Transaction(
        amount=data.amount,
        description=data.description,
        type=data.type,
        category_id=data.category_id,
        user_id=user_id,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


async def get_transactions(
    db: AsyncSession,
    user_id: int,
    category_id: int | None = None,
    type: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Transaction]:
    query = select(Transaction).where(Transaction.user_id == user_id)

    if category_id:
        query = query.where(Transaction.category_id == category_id)
    if type:
        query = query.where(Transaction.type == type)
    if date_from:
        query = query.where(Transaction.created_at >= date_from)
    if date_to:
        query = query.where(Transaction.created_at <= date_to)

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    return list(result.scalars().all())


async def count_transactions(
    db: AsyncSession,
    user_id: int,
    category_id: int | None = None,
    type: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> int:
    query = select(func.count(Transaction.id)).where(Transaction.user_id == user_id)

    if category_id:
        query = query.where(Transaction.category_id == category_id)
    if type:
        query = query.where(Transaction.type == type)
    if date_from:
        query = query.where(Transaction.created_at >= date_from)
    if date_to:
        query = query.where(Transaction.created_at <= date_to)

    result = await db.execute(query)
    return result.scalar()


async def get_transaction_by_id(db: AsyncSession, transaction_id: int, user_id: int) -> Transaction | None:
    result = await db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def update_transaction(db: AsyncSession, transaction_id: int, user_id: int, data: TransactionUpdate) -> Transaction | None:
    transaction = await get_transaction_by_id(db, transaction_id, user_id)
    if not transaction:
        return None

    updated_data = data.model_dump(exclude_unset=True)

    #чекаем что юзер мог дать не существующий айди
    if "category_id" in updated_data:
        category = await get_category_by_id(db, updated_data["category_id"])
        if not category:
            raise ValueError("Category not found")

    for key, value in updated_data.items():
        setattr(transaction, key, value)

    await db.commit()
    await db.refresh(transaction)
    return transaction


async def delete_transaction(db: AsyncSession, transaction_id: int, user_id: int) -> bool:
    transaction = await get_transaction_by_id(db, transaction_id, user_id)
    if not transaction:
        return False

    await db.delete(transaction)
    await db.commit()
    return True


async def get_statistics(
    db: AsyncSession,
    user_id: int,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    query = select(
        Transaction.type,
        func.sum(Transaction.amount)
    ).where(Transaction.user_id == user_id).group_by(Transaction.type)

    if date_from:
        query = query.where(Transaction.created_at >= date_from)
    if date_to:
        query = query.where(Transaction.created_at <= date_to)

    result = await db.execute(query)
    rows = result.all()

    total_income = 0.0
    total_expense = 0.0
    for type, amount in rows:
        if type == "income":
            total_income = float(amount)
        elif type == "expense":
            total_expense = float(amount)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
    }
