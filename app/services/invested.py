from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def _process_donation(session: AsyncSession, donation, new_project):
    if donation.full_amount <= new_project.full_amount:
        residual_amount = new_project.full_amount - donation.full_amount
        new_project.full_amount = residual_amount
        donation.invested_amount = donation.full_amount
        new_project.invested_amount += donation.full_amount
        donation.full_amount = 0
        donation.fully_invested = True
        donation.close_date = datetime.utcnow()
        session.add(donation)
        if new_project.full_amount == 0:
            new_project.fully_invested = True
            new_project.close_date = datetime.utcnow()
            session.add(new_project)
            return True
        session.add(new_project)
    else:
        residual_amount = donation.full_amount - new_project.full_amount
        donation.full_amount = residual_amount
        new_project.invested_amount = new_project.full_amount
        donation.invested_amount += new_project.full_amount
        new_project.full_amount = 0
        new_project.fully_invested = True
        new_project.close_date = datetime.utcnow()
        session.add(donation)
        session.add(new_project)
    return False


async def _process_project(session: AsyncSession, project, new_donation):
    if project.full_amount <= new_donation.full_amount:
        residual_amount = new_donation.full_amount - project.full_amount
        new_donation.full_amount = residual_amount
        project.invested_amount = project.full_amount
        new_donation.invested_amount += project.full_amount
        project.full_amount = 0
        project.fully_invested = True
        project.close_date = datetime.utcnow()
        session.add(project)
        if new_donation.full_amount == 0:
            new_donation.fully_invested = True
            new_donation.close_date = datetime.utcnow()
            session.add(new_donation)
            return True
        session.add(new_donation)
    else:
        residual_amount = project.full_amount - new_donation.full_amount
        project.full_amount = residual_amount
        new_donation.invested_amount = new_donation.full_amount
        project.invested_amount += new_donation.full_amount
        new_donation.full_amount = 0
        new_donation.fully_invested = True
        new_donation.close_date = datetime.utcnow()
        session.add(project)
        session.add(new_donation)
    return False


async def invest_in_project(
        session: AsyncSession,
        new_project=None,
        new_donation=None,
):
    if new_project:
        donations = await session.execute(
            select(Donation).where(Donation.fully_invested == 0))
        donations = donations.scalars().all()
        for donation in donations:
            if await _process_donation(session, donation, new_project):
                break

    elif new_donation:
        projects = await session.execute(
            select(
                CharityProject).where(
                    CharityProject.fully_invested == 0))
        projects = projects.scalars().all()
        for project in projects:
            if await _process_project(session, project, new_donation):
                break

    await session.commit()
    if new_project:
        await session.refresh(new_project)
        return new_project
    elif new_donation:
        await session.refresh(new_donation)
        return new_donation
    return None
