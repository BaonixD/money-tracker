from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey

from backend.database import Base

class Transaction(Base):

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(nullable=False)

    # связь с категорией
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # связь с юзером
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    category: Mapped["Category"] = relationship(back_populates="transactions")
    user: Mapped["User"] = relationship(back_populates="transactions")


