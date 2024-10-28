from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        return (
            await session.execute(
                select(self.model).where(self.model.id == obj_id))
        ).scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        return (await session.execute(select(self.model))).scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            for_commit: bool = True
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        if not for_commit:
            obj_in_data['invested_amount'] = 0
            obj_in_data['fully_invested'] = False
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if for_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
            for_commit: bool = True
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if for_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def open_objects(
            self,
            model,
            session: AsyncSession,
    ):
        return (await session.execute(
            select(model).where(model.fully_invested == 0)
        )).scalars().all()
