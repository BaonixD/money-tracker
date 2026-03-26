import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

class TransactionCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    type: str
    category_id: int

    @field_validator("type")
    @classmethod
    def validate_type_name(cls, v: str):
        if v not in ["income", "expense"]:
            raise ValueError("Type must be either 'income' or 'expense'")
        return v



class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    type: Optional[str] = None
    category_id: Optional[int] = None

    @field_validator("type")
    @classmethod
    def validate_type_name(cls, v: str | None):
        if v is not None and v not in ["income", "expense"]:
            raise ValueError("Type must be either 'income' or 'expense'")
        return v


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    type: str
    category_id: int
    user_id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)



