from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, conint, constr


class CharityprojectBase(BaseModel):
    invested_amount: int = Field(0)
    fully_invested: bool
    create_date: datetime = Field(datetime.now() + timedelta(minutes=10))
    close_date: Optional[datetime]


class CharityprojectCreate(BaseModel):
    name: constr(strict=True, min_length=1, max_length=100) = Field(...)
    description: constr(strict=True, min_length=1) = Field(...)
    full_amount: conint(strict=True, gt=0) = Field(...)

    class Config:
        extra = Extra.forbid


class CharityprojectUpdate(CharityprojectCreate):
    name: constr(strict=True, min_length=1, max_length=100) = None
    description: constr(strict=True, min_length=1) = None
    full_amount: conint(strict=True, gt=0) = None


class CharityprojectDB(CharityprojectBase, CharityprojectCreate):
    id: int
    full_amount: int

    class Config:
        orm_mode = True
