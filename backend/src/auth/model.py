import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, MappedColumn
from sqlalchemy.orm import mapped_column

from backend.database import Base

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(ullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.utcnow
    )