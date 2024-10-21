from sqlalchemy import Column, String, Text

# from sqlalchemy.orm import relationship

from app.models.base_model import BaseModelApp


class CharityProject(BaseModelApp):
    # уникальное название проекта, обязательное строковое поле,
    # допустимая длина строки — от 1 до 100 символов включительно.
    name = Column(String(100), unique=True, nullable=False)
    #  не менее одного символа
    description = Column(Text, nullable=False)
