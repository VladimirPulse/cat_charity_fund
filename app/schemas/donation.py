from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, conint, constr


class DonationBase(BaseModel):
    invested_amount: int = Field(0)
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]


class DonationCreate(BaseModel):
    comment: Optional[constr(strict=True)] = None
    full_amount: conint(strict=True, gt=0) = Field(...)

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate, DonationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class DonationCreateDB(DonationCreate):
    id: int
    create_date: datetime
    full_amount: int

    class Config:
        orm_mode = True
