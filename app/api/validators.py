from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject
from app.schemas.charityproject import CharityprojectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_project_full_amount(
        project_id: int,
        full_amount: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нелья установить значение '
            'full_amount меньше уже вложенной суммы.'
        )
    return project


def check_project_remove(
        project: CharityProject,
) -> CharityProject:
    if project.fully_invested or project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


def check_project_update(
        project: CharityProject,
        obj_in: CharityprojectUpdate
) -> CharityProject:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект был закрыт, не подлежит редактированию!'
        )
    if obj_in.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    return project
