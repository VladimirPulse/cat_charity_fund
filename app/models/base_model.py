from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class BaseModelForProectsDonacions(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            'full_amount >= 0',
            name='check_invested_amount_positive'
        ),
        CheckConstraint(
            'fully_invested = TRUE OR invested_amount <= full_amount',
            name='check_invested_amount_limit'
        )
    )

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}(full_amount={self.full_amount}, )>'
            f'<invested_amount={self.invested_amount}, >'
            f'fully_invested={self.fully_invested})>'
        )

    def __str__(self):
        return (
            f'{self.__class__.__name__} with Full Amount: '
            f'{self.full_amount}, Invested Amount: {self.invested_amount}, '
            f'Fully Invested: {self.fully_invested}'
        )
