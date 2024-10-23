from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, conint, constr, validator


# Базовый класс схемы, от которого наследуем все остальные.
class CharityprojectBase(BaseModel):
    # требуемая сумма, целочисленное поле; больше 0
    # full_amount: StrictInt = Field(...)
    # целочисленное поле; значение по умолчанию — 0
    invested_amount: int = Field(0)
    # булево значение, значение по умолчанию — False
    fully_invested: bool
    # должно добавляться автоматически в момент создания проекта
    create_date: datetime
    # проставляется автоматически в момент набора нужной суммы
    close_date: Optional[datetime] #= Field(...)


# Теперь наследуем схему не от BaseModel, а от MeetingRoomBase.
class CharityprojectCreate(BaseModel):
    # Переопределяем атрибут name, делаем его обязательным.
    name: constr(strict=True, min_length=1, max_length=100) = Field(...)
    #  не менее одного символа
    description: constr(strict=True, min_length=1) = Field(...)
    full_amount: conint(strict=True, gt=0) = Field(...)

    class Config:
        extra = Extra.forbid

    # @validator('name')
    # def name_cant_be_numeric(cls, value: str):
    #     num = 0
    #     for _ in value:
    #         num += 1
    #     if value == '' or num > 100:
    #         raise ValueError(
    #             'Имя не может быть '
    #             'пустым или содержать '
    #             'более 100 символов'
    #         )
    #     return value 
# Новый класс для обновления объектов.
class CharityprojectUpdate(CharityprojectCreate):
    pass

    # @validator('name')
    # def name_cannot_be_null(cls, value):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value

# Возвращаемую схему унаследуем от MeetingRoomCreate, 
# чтобы снова не описывать обязательное поле name.
class CharityprojectDB(CharityprojectBase, CharityprojectCreate):
    id: int 
    full_amount: int

    class Config:
        orm_mode = True 
