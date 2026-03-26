import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(BaseModel):

    name: str
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

