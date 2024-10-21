from sqlalchemy import Column, Integer, DateTime, Boolean
from datetime import datetime

from app.core.db import Base


class BaseModelApp(Base):
    __abstract__ = True  # Указываем, что этот класс абстрактный
    # требуемая сумма, целочисленное поле; больше 0
    full_amount = Column(Integer, nullable=False)
    # целочисленное поле; значение по умолчанию — 0
    invested_amount = Column(Integer, default=0)
    # булево значение, значение по умолчанию — False
    fully_invested  = Column(Boolean, default=False)
    # должно добавляться автоматически в момент создания проекта
    create_date = Column(DateTime, default=datetime.utcnow)
    # проставляется автоматически в момент набора нужной суммы
    close_date = Column(DateTime)
