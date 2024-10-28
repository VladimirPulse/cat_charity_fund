from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class BaseModelCatFund(Base):
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
            '(invested_amount >= 0 AND invested_amount <= full_amount) '
            'OR (invested_amount > 0 AND full_amount = 0)',
            name='check_invested_amount_limit'
        )
    )

    def __repr__(self):
        return (
            f'<{type(self).__name__}(full_amount={self.full_amount})>, '
            f'<invested_amount={self.invested_amount}>, '
            f'<fully_invested={self.fully_invested})>'
        )

    def __str__(self):
        return (
            f'{type(self).__name__}, '
            f'{self.full_amount=}, {self.invested_amount=}, '
            f'{self.fully_invested=}'
        )
