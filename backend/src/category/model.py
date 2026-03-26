from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from backend.database import Base


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")
