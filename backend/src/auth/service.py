from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.auth.model import User
from backend.src.auth.schemas import UserCreate
from backend.src.auth.utils import hash_password, verify_password

async def create_user ( db: AsyncSession, user_data: UserCreate ) -> User:
    user = User (
        email=user_data.email,
        username=user_data.username,
        hashed_password = hash_password(user_data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email ( db: AsyncSession, email : str) -> User | None:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def authenticate_user ( db: AsyncSession, email: str, password: str ) -> User | None:
    user = await get_user_by_email ( db, email )

    if not user or not verify_password ( password, user.hashed_password ):
        return None
    return user