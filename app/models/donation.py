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
        return (
            f'{super().__repr__()}, {self.comment=}, {self.user_id=}'
        )
