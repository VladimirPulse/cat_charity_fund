from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


# Создаем новый класс, унаследованный от CRUDBase.
class CRUDCharityProject(CRUDBase):

    # Преобразуем функцию в метод класса.
    async def get_project_id_by_name(
            # Дописываем параметр self. 
            # В качестве альтернативы здесь можно 
            # применить декоратор @staticmethod.
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    
# Объект crud наследуем уже не от CRUDBase, 
# а от только что созданного класса CRUDMeetingRoom. 
# Для инициализации передаем модель, как и в CRUDBase.
charity_project_crud = CRUDCharityProject(CharityProject)