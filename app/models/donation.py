from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base_model import BaseModelCatFund


class Donation(BaseModelCatFund):
    __tablename__ = 'donation'
    comment = Column(String)
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr}, Comment: {self.comment}, User ID: {self.user_id}'
