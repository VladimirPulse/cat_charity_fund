from sqlalchemy import Column, String, Text

from app.models.base_model import BaseModelCatFund


class CharityProject(BaseModelCatFund):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{super().__repr__()}, {self.name=}, {self.description=}'
        )
