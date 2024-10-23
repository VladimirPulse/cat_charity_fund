# from sqlalchemy.ext.asyncio import AsyncSession
# from datetime import datetime

# from app.models.charityproject import CharityProject
# from app.models.donation import Donation

# async def invest_in_project(
# # def invest_in_project(
#         session: AsyncSession,
#         project: CharityProject
# ):
#     # project = session.query(CharityProject).filter(CharityProject.id == project_id).first()
#     if not project:
#         return
#     # Получаем все свободные пожертвования
#     donations = session.query(Donation).filter(Donation.fully_invested == False).all()
#     for donation in donations:
#         if project.fully_invested:
#             break
#         available_amount = donation.full_amount - donation.invested_amount
#         if available_amount <= 0:
#             continue
#         # Определяем, сколько можно инвестировать в проект
#         amount_to_invest = min(available_amount, project.full_amount - project.invested_amount)
#         # Обновляем суммы
#         donation.invested_amount += amount_to_invest
#         project.invested_amount += amount_to_invest
#         # Проверяем, достигнута ли полная сумма
#         if project.invested_amount >= project.full_amount:
#             project.fully_invested = True
#             project.close_date = datetime.utcnow()
#     session.commit()
#     session.refresh(project)
#     return project


# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.orm import selectinload
# from sqlalchemy import update
# from fastapi import HTTPException
# from datetime import datetime

# from app.models.charityproject import CharityProject
# from app.models.donation import Donation

# async def invest_in_project(
#         # *,
#         session: AsyncSession,
#         new_project=None,
#         new_donation=None,
# ):
#     invested_amount = 0
    
#     if new_project:
#         # 1. Автоматически инвестируем все "свободные" суммы из пожертвований
#         donations = await session.execute(select(Donation).where(Donation.fully_invested == False))
#         donations = donations.scalars().all()
#         for donation in donations:
#             if invested_amount + donation.full_amount <= new_project.full_amount:
#                 invested_amount += donation.full_amount
#                 donation.invested_amount += donation.full_amount
#                 donation.fully_invested = True
#                 donation.close_date = datetime.utcnow()
#                 new_project.invested_amount += donation.full_amount
#                 # Сохраняем изменения
#                 session.add(donation)
#                 print(f"Инвестировано из пожертвования {donation.id}: {donation.full_amount}")
#             else:
#                 residual_amount = new_project.full_amount - new_project.invested_amount
#                 invested_amount += residual_amount
#                 donation.invested_amount += residual_amount
#                 donation.fully_invested = False  # В этом случае часть суммы не инвестирована.
#                 donation.close_date = None  # Снова помещаем в открытое состояние.
#                 new_project.invested_amount += residual_amount
#                 # Сохраняем изменения
#                 session.add(donation)
#                 print(f"Инвестировано частично из пожертвования {donation.id}: {residual_amount}")
#             if new_project.invested_amount >= new_project.full_amount:
#                 new_project.fully_invested = True
#                 new_project.close_date = datetime.utcnow()
#                 break  # Проект полностью профинансирован.
#     elif new_donation:
#         # 2. Автоматически зачисляем пожертвования на открытые проекты
#         projects = await session.execute(select(CharityProject).where(CharityProject.fully_invested == False))
#         projects = projects.scalars().all()
#         for project in projects:
#             if invested_amount + new_donation.full_amount <= project.full_amount:
#                 invested_amount += new_donation.full_amount
#                 project.invested_amount += new_donation.full_amount
#                 new_donation.invested_amount += new_donation.full_amount
#                 new_donation.fully_invested = True
#                 # Сохраняем изменения
#                 session.add(new_donation)
#                 session.add(project)
#                 print(f"Инвестировано в проект {project.id}: {new_donation.full_amount}")
#             else:
#                 residual_amount = project.full_amount - project.invested_amount
#                 invested_amount += residual_amount
#                 project.invested_amount += residual_amount
#                 new_donation.invested_amount += residual_amount
#                 new_donation.fully_invested = False
#                 # Сохраняем изменения
#                 session.add(new_donation)
#                 session.add(project)
#                 print(f"Инвестировано частично в проект {project.id}: {residual_amount}")
#             if project.invested_amount >= project.full_amount:
#                 project.fully_invested = True
#                 project.close_date = datetime.utcnow()
#                 break  # Проект полностью профинансирован.
#     # Коммитим все изменения одной транзакцией
#     await session.commit()
#     # Обновляем и возвращаем нужные объекты
#     if new_project:
#         await session.refresh(new_project)
#         return new_project
#     elif new_donation:
#         await session.refresh(new_donation)
#         return new_donation
#     return None

def calculation(arg_1, arg_2):
    args = {}
    if arg_1.full_amount <= arg_2.full_amount:
        residual_amount = arg_2.full_amount - arg_1.full_amount
        arg_2.full_amount = residual_amount
        arg_1.invested_amount = arg_1.full_amount
        arg_2.invested_amount = arg_1.full_amount
        arg_1.full_amount = 0
    else:
        residual_amount = arg_1.full_amount - arg_2.full_amount
        arg_1.full_amount = residual_amount
        arg_2.invested_amount = arg_2.full_amount
        arg_1.invested_amount = arg_2.full_amount
        arg_2.full_amount = 0
    if arg_2.full_amount == 0:
        arg_2.fully_invested = True
        arg_2.close_date = datetime.utcnow()
    if arg_1.full_amount == 0:
        arg_1.fully_invested = True
        arg_1.close_date = datetime.utcnow()
    args['arg_1'] = arg_1
    args['arg_2'] = arg_2
    return args

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update
from fastapi import HTTPException
from datetime import datetime

from app.models.charityproject import CharityProject
from app.models.donation import Donation

async def invest_in_project(
        # *,
        session: AsyncSession,
        new_project=None,
        new_donation=None,
):
    if new_project:
        # 1. Автоматически инвестируем все "свободные" суммы из пожертвований
        donations = await session.execute(select(Donation).where(Donation.fully_invested == False))
        donations = donations.scalars().all()
        for donation in donations:
            if donation.full_amount <= new_project.full_amount:
                residual_amount = new_project.full_amount - donation.full_amount
                new_project.full_amount = residual_amount
                donation.invested_amount = donation.full_amount
                new_project.invested_amount = donation.full_amount
                donation.full_amount = 0
                donation.fully_invested = True
                donation.close_date = datetime.utcnow()
                session.add(donation)
                if new_project.full_amount == 0:
                    new_project.fully_invested = True
                    new_project.close_date = datetime.utcnow()
                    session.add(new_project)
                    break  # Проект полностью профинансирован.
                session.add(new_project)
            else:
                residual_amount = donation.full_amount - new_project.full_amount
                donation.full_amount = residual_amount
                new_project.invested_amount = new_project.full_amount
                donation.invested_amount = new_project.full_amount
                new_project.full_amount = 0
                new_project.fully_invested = True
                new_project.close_date = datetime.utcnow()
                session.add(donation)
                session.add(new_project)
    elif new_donation:
        # 2. Автоматически зачисляем пожертвования на открытые проекты
        projects = await session.execute(select(CharityProject).where(CharityProject.fully_invested == False))
        projects = projects.scalars().all()
        for project in projects:
            if project.full_amount <= new_donation.full_amount:
                residual_amount = new_donation.full_amount - project.full_amount
                new_donation.full_amount = residual_amount
                project.invested_amount = project.full_amount
                new_donation.invested_amount = project.full_amount
                project.full_amount = 0
                project.fully_invested = True
                project.close_date = datetime.utcnow()
                session.add(project)
                if new_donation.full_amount == 0:
                    new_donation.fully_invested = True
                    new_donation.close_date = datetime.utcnow()
                    session.add(new_donation)
                    break  # Проект полностью профинансирован.
                session.add(new_donation)
            else:
                residual_amount = project.full_amount - new_donation.full_amount
                project.full_amount = residual_amount
                new_donation.invested_amount = new_donation.full_amount
                project.invested_amount = new_donation.full_amount
                new_donation.full_amount = 0
                new_donation.fully_invested = True
                new_donation.close_date = datetime.utcnow()
                session.add(project)
                session.add(new_donation)
    # Коммитим все изменения одной транзакцией
    await session.commit()
    # Обновляем и возвращаем нужные объекты
    if new_project:
        await session.refresh(new_project)
        return new_project
    elif new_donation:
        await session.refresh(new_donation)
        return new_donation
    return None
