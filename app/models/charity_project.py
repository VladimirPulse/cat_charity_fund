from sqlalchemy import Column, String, Text

from app.models.base_model import BaseModelApp


class CharityProject(BaseModelApp):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
