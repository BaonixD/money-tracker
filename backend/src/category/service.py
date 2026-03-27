from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.category.model import Category
from backend.src.category.schemas import CategoryCreate


async def create_category(db: AsyncSession, data: CategoryCreate) -> Category:
    category = Category(name=data.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_categories(db: AsyncSession) -> list[Category]:
    result = await db.execute(select(Category))
    return list(result.scalars().all())


async def get_category_by_id(db: AsyncSession, category_id: int) -> Category | None:
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    return result.scalar_one_or_none()
