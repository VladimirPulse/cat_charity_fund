from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_remove,
    check_name_duplicate,
    check_project_exists,
    check_project_full_amount,
    check_project_update
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (
    CharityprojectCreate, CharityprojectDB, CharityprojectUpdate
)
from app.services.invested import invest_in_project

router = APIRouter()


@router.post(
    '/',
    response_model=CharityprojectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityprojectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(
        charity_project, session)
    new_project = await invest_in_project(
        new_project=charity_project, session=session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityprojectDB]
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session),
):
    all_rooms = await charity_project_crud.get_multi(session)
    return all_rooms


@router.patch(
    '/{project_id}',
    response_model=CharityprojectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityprojectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_project_full_amount(
            project_id, obj_in.full_amount, session)
    project = await check_project_update(project, obj_in)
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    new_project = await invest_in_project(new_project=project, session=session)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityprojectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )
    await check_project_remove(project)
    project = await charity_project_crud.remove(project, session)
    return project
