from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationCreateDB, DonationDB
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
    db_donation = await donation_crud.create(
        donation, session, user, for_commit=False)
    session.add_all(
        invest_in_project(
            target=db_donation,
            sources=await donation_crud.open_objects(
                CharityProject, session)
        )
    )
    await session.commit()
    await session.refresh(db_donation)
    return db_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationCreateDB],
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Только для авторизованных."""
    return await donation_crud.get_by_user(session, user)
