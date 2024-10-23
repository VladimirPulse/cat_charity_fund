from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationCreateDB
)
from app.services.invested import invest_in_project

router = APIRouter() 


@router.post(
    '/',
    response_model=DonationCreateDB,
    dependencies=[Depends(current_user)],
)
async def create_new_charity_project(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Только для авторизованных."""
    await check_name_duplicate(donation.full_amount, session)
    db_donation = await donation_crud.create(donation, session, user)
    new_donation = await invest_in_project(new_donation=db_donation, session=session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationCreateDB],
    # dependencies=[Depends(current_user)],
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Только для авторизованных."""
    all_donations = await donation_crud.get_by_user(session, user)
    return all_donations


# @router.delete(
#     '/{donation_id}',
#     response_model=DonationDB,
#     dependencies=[Depends(current_superuser)],
# )
# async def remove_project(
#         donation_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     """Только для суперюзеров."""
#     project = await donation_crud.get(donation_id, session)
#     project = await donation_crud.remove(project, session)
#     return project
