from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.transactions.model import Transaction
from backend.src.transactions.schemas import TransactionCreate
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


async def get_transactions(db: AsyncSession, user_id: int) -> list[Transaction]:
    result = await db.execute(
        select(Transaction).where(Transaction.user_id == user_id)
    )
    return list(result.scalars().all())


async def get_transaction_by_id(db: AsyncSession, transaction_id: int, user_id: int) -> Transaction | None:
    result = await db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()
