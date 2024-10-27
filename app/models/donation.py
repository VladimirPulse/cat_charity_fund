from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base_model import BaseModelForProectsDonacions


class Donation(BaseModelForProectsDonacions):
    __tablename__ = 'donation'
    comment = Column(String)
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr}, Comment: {self.comment}, User ID: {self.user_id}'

    def __str__(self):
        base_str = super().__str__()
        return f'{base_str}, Comment: {self.comment}, User ID: {self.user_id}'
