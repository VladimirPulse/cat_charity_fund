from sqlalchemy import Column, String, Text

from app.models.base_model import BaseModelForProectsDonacions


class CharityProject(BaseModelForProectsDonacions):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        base_repr = super().__repr__()
        return (
            f'{base_repr}, Name: {self.name}, Description: {self.description}'
        )

    def __str__(self):
        base_str = super().__str__()
        return (
            f'{base_str}, Name: {self.name}, '
            f'Description ID: {self.description}'
        )
