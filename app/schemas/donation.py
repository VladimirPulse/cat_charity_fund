from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, conint, constr, validator


# Базовый класс схемы, от которого наследуем все остальные.
class DonationBase(BaseModel):
    # требуемая сумма, целочисленное поле; больше 0
    # целочисленное поле; значение по умолчанию — 0
    invested_amount: int = Field(0)
    # булево значение, значение по умолчанию — False
    fully_invested: bool
    # должно добавляться автоматически в момент создания проекта
    create_date: datetime
    # проставляется автоматически в момент набора нужной суммы
    close_date: Optional[datetime] #= Field(...)


class DonationCreate(BaseModel):
    comment: Optional[constr(strict=True)] = None
    full_amount: conint(strict=True, gt=0) = Field(...)

    class Config:
        extra = Extra.forbid

    # class Config:
    #     extra = Extra.forbid

class DonationDB(DonationCreate, DonationBase):
    id: int 
    user_id: int

    class Config:
        orm_mode = True 

class DonationCreateDB(DonationCreate):
    id: int 
    create_date: datetime

    class Config:
        orm_mode = True 
