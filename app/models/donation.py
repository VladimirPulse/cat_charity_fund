from sqlalchemy import Column, String, ForeignKey, Integer

from app.models.base_model import BaseModelApp


class Donation(BaseModelApp):
    __tablename__ = 'donation'
    comment = Column(String)
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
